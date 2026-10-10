use clap::Parser;
use minijinja::Environment;
use std::net::SocketAddr;
use std::path::Path;
use std::sync::Arc;
use timeseek::cache::EntryCache;
use timeseek::db::Database;
use timeseek::ml::VectorEmbeddingEngine;
use timeseek::recording::{RecorderConfig, ScreenRecorder};
use timeseek::state::AppState;
use timeseek::web::{create_router, AppContext};
use tracing::{info, Level};
use tracing_subscriber::FmtSubscriber;

#[derive(Parser, Debug)]
#[command(
    author,
    version,
    about = "Privacy-first offline digital memory & screen recording system written in Rust"
)]
struct Args {
    #[arg(short, long, default_value_t = 8082)]
    port: u16,

    #[arg(short, long, default_value = "timeseek.db")]
    db_path: String,

    #[arg(short, long, default_value = "images")]
    screenshots_path: String,

    #[arg(short, long, default_value = "")]
    blacklist: String,

    #[arg(short, long, default_value = "")]
    keyword_blacklist: String,

    #[arg(short, long, default_value_t = 30)]
    retention_days: u64,

    #[arg(long, default_value_t = false)]
    primary_monitor_only: bool,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let subscriber = FmtSubscriber::builder()
        .with_max_level(Level::INFO)
        .finish();
    tracing::subscriber::set_global_default(subscriber)?;

    let args = Args::parse();
    info!("Starting Timeseek Rust v{}", env!("CARGO_PKG_VERSION"));

    let db = Arc::new(Database::new(&args.db_path)?);
    let state = Arc::new(AppState::new());
    let cache = EntryCache::new();
    let ml_engine = Arc::new(VectorEmbeddingEngine::new());

    // Auto-prune old data on startup
    if let Ok(count) = db.prune_old_data(args.retention_days, &args.screenshots_path) {
        if count > 0 {
            info!(
                "Auto-pruned {} entries older than {} days",
                count, args.retention_days
            );
        }
    }

    // Populate initial cache
    if let Ok(entries) = db.get_all_entries() {
        cache.set(entries);
    }

    // Minijinja setup & custom filters
    let mut jinja_env = Environment::new();
    jinja_env.add_filter("timestamp_to_human_readable", |ts: i64| -> String {
        if ts <= 0 {
            return "N/A".to_string();
        }
        if let Some(datetime) = chrono::DateTime::from_timestamp(ts, 0) {
            datetime.format("%Y-%m-%d %H:%M:%S").to_string()
        } else {
            "N/A".to_string()
        }
    });

    jinja_env.add_filter("human_readable_time", |seconds: u64| -> String {
        if seconds < 60 {
            format!("{}s", seconds)
        } else if seconds < 3600 {
            format!("{}m", seconds / 60)
        } else {
            let hours = seconds / 3600;
            let mins = (seconds % 3600) / 60;
            if mins > 0 {
                format!("{}h {}m", hours, mins)
            } else {
                format!("{}h", hours)
            }
        }
    });

    jinja_env.add_filter("get_app_category", |app_name: String| -> String {
        let app_lower = app_name.to_lowercase();
        if app_lower.contains("code") || app_lower.contains("terminal") || app_lower.contains("cargo") {
            "Development".to_string()
        } else if app_lower.contains("firefox") || app_lower.contains("chrome") || app_lower.contains("browser") {
            "Browsing".to_string()
        } else {
            "General".to_string()
        }
    });

    let templates_dir = Path::new("timeseek/templates");
    if templates_dir.exists() {
        for entry in std::fs::read_dir(templates_dir)? {
            let entry = entry?;
            let path = entry.path();
            if path.is_file() {
                if let Some(name) = path.file_name().and_then(|s| s.to_str()) {
                    if let Ok(content) = std::fs::read_to_string(&path) {
                        let _ = jinja_env.add_template_owned(name.to_string(), content);
                    }
                }
            }
        }
    }

    let blacklisted_apps: Vec<String> = args
        .blacklist
        .split(',')
        .map(|s| s.trim().to_string())
        .filter(|s| !s.is_empty())
        .collect();

    let blacklisted_keywords: Vec<String> = args
        .keyword_blacklist
        .split(',')
        .map(|s| s.trim().to_string())
        .filter(|s| !s.is_empty())
        .collect();

    let recorder_config = RecorderConfig {
        screenshots_dir: args.screenshots_path.clone(),
        db_path: args.db_path.clone(),
        blacklisted_apps,
        blacklisted_keywords,
        primary_monitor_only: args.primary_monitor_only,
        image_quality: 80,
    };

    let recorder = Arc::new(ScreenRecorder::new(
        recorder_config,
        Arc::clone(&state),
        Arc::clone(&db),
        cache.clone(),
    ));

    // Spawn screen recorder in background
    tokio::spawn(async move {
        recorder.run_loop().await;
    });

    let app_ctx = AppContext {
        db,
        cache,
        state,
        jinja_env: Arc::new(jinja_env),
        ml_engine,
        screenshots_dir: args.screenshots_path,
    };

    let router = create_router(app_ctx);
    let addr = SocketAddr::from(([0, 0, 0, 0], args.port));
    info!("Server listening on http://localhost:{}", args.port);

    let listener = tokio::net::TcpListener::bind(addr).await?;
    axum::serve(listener, router).await?;

    Ok(())
}
