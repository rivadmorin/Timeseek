use crate::cache::EntryCache;
use crate::db::Database;
use crate::ml::{cosine_similarity, VectorEmbeddingEngine};
use crate::state::AppState;
use axum::{
    extract::{Form, Path as AxumPath, Query, State},
    http::StatusCode,
    response::{Html, IntoResponse, Redirect},
    routing::{get, post},
    Json, Router,
};
use minijinja::Environment;
use serde::Deserialize;
use serde_json::json;
use std::collections::HashMap;
use std::path::Path;
use std::sync::Arc;
use std::time::{SystemTime, UNIX_EPOCH};
use tower_http::services::ServeDir;
use tracing::error;

#[derive(Clone)]
pub struct AppContext {
    pub db: Arc<Database>,
    pub cache: EntryCache,
    pub state: Arc<AppState>,
    pub jinja_env: Arc<Environment<'static>>,
    pub ml_engine: Arc<VectorEmbeddingEngine>,
    pub screenshots_dir: String,
}

#[derive(Deserialize)]
pub struct SearchQuery {
    pub q: Option<String>,
    pub app: Option<String>,
}

#[derive(Deserialize)]
pub struct NotesRequest {
    pub notes: String,
}

#[derive(Deserialize)]
pub struct DeleteRangeRequest {
    pub start_timestamp: i64,
    pub end_timestamp: i64,
}

#[derive(Deserialize)]
pub struct BulkDeleteForm {
    pub range: u64,
}

#[derive(Deserialize)]
pub struct DeleteAppRequest {
    pub app_name: String,
}

#[derive(Deserialize)]
pub struct SettingsRequest {
    pub recording_paused: Option<bool>,
}

pub fn create_router(ctx: AppContext) -> Router {
    Router::new()
        .route("/", get(handle_index))
        .route("/dashboard", get(handle_index))
        .route("/timeline", get(handle_timeline))
        .route("/search", get(handle_search_page))
        .route("/settings", get(handle_settings_page))
        .route("/snapshot/:id", get(handle_snapshot_detail))
        .route("/export/pdf/:id", get(handle_export_pdf))
        .route("/update_note/:id", post(handle_update_note))
        .route("/delete/:id", post(handle_delete_single))
        .route("/bulk_delete", post(handle_bulk_delete))
        .route("/purge", post(handle_purge))
        .route("/api/dashboard", get(handle_api_dashboard))
        .route("/api/timeline", get(handle_api_timeline))
        .route("/api/search", get(handle_api_search))
        .route("/api/heatmap", get(handle_api_heatmap))
        .route("/api/wordcloud", get(handle_api_wordcloud))
        .route("/api/settings", post(handle_api_settings))
        .route("/api/entries/:id/notes", post(handle_api_notes))
        .route("/api/entries/:id/favorite", post(handle_api_favorite))
        .route("/api/delete_range", post(handle_api_delete_range))
        .route("/api/delete_app", post(handle_api_delete_app))
        .route("/api/purge", post(handle_api_purge))
        .nest_service("/static", ServeDir::new("timeseek/static"))
        .nest_service("/screenshots", ServeDir::new(&ctx.screenshots_dir))
        .with_state(ctx)
}

fn format_human_readable_time(seconds: u64) -> String {
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
}

async fn handle_index(State(ctx): State<AppContext>) -> impl IntoResponse {
    let entries = ctx.cache.get_all();
    let total_snapshots = entries.len();
    let total_time_human = format_human_readable_time((total_snapshots * 3) as u64);

    let mut app_counts: HashMap<String, usize> = HashMap::new();
    for entry in &entries {
        if !entry.app.is_empty() {
            *app_counts.entry(entry.app.clone()).or_insert(0) += 1;
        }
    }

    let mut top_apps: Vec<(String, usize)> = app_counts.into_iter().collect();
    top_apps.sort_by(|a, b| b.1.cmp(&a.1));
    top_apps.truncate(5);

    render_template(
        &ctx.jinja_env,
        "dashboard.html",
        json!({
            "total_snapshots": total_snapshots,
            "total_time_human": total_time_human,
            "top_apps": top_apps,
            "is_paused": ctx.state.is_recording_paused(),
        }),
    )
}

async fn handle_timeline(State(ctx): State<AppContext>) -> impl IntoResponse {
    let entries = ctx.cache.get_all();
    let entries_json = serde_json::to_string(&entries).unwrap_or_else(|_| "[]".to_string());

    render_template(
        &ctx.jinja_env,
        "timeline.html",
        json!({
            "entries": entries,
            "entries_json": entries_json,
        }),
    )
}

async fn handle_search_page(
    State(ctx): State<AppContext>,
    Query(query): Query<SearchQuery>,
) -> impl IntoResponse {
    let q = query.q.unwrap_or_default();
    let selected_app = query.app.unwrap_or_default();
    let all_entries = ctx.cache.get_all();

    let mut apps_set: std::collections::BTreeSet<String> = std::collections::BTreeSet::new();
    for entry in &all_entries {
        if !entry.app.is_empty() {
            apps_set.insert(entry.app.clone());
        }
    }
    let apps: Vec<String> = apps_set.into_iter().collect();

    let filtered_entries: Vec<_> = all_entries
        .into_iter()
        .filter(|e| {
            let app_matches = selected_app.is_empty() || e.app.to_lowercase() == selected_app.to_lowercase();
            let text_matches = q.is_empty()
                || e.text.to_lowercase().contains(&q.to_lowercase())
                || e.title.to_lowercase().contains(&q.to_lowercase())
                || e.app.to_lowercase().contains(&q.to_lowercase())
                || e.notes.to_lowercase().contains(&q.to_lowercase());
            app_matches && text_matches
        })
        .collect();

    render_template(
        &ctx.jinja_env,
        "search.html",
        json!({
            "entries": filtered_entries,
            "apps": apps,
            "current_app": selected_app,
            "q": q,
        }),
    )
}

async fn handle_settings_page(State(ctx): State<AppContext>) -> impl IntoResponse {
    render_template(
        &ctx.jinja_env,
        "settings.html",
        json!({
            "is_paused": ctx.state.is_recording_paused(),
        }),
    )
}

async fn handle_snapshot_detail(
    State(ctx): State<AppContext>,
    AxumPath(id): AxumPath<i64>,
) -> impl IntoResponse {
    let entries = ctx.cache.get_all();
    let entry = entries.into_iter().find(|e| e.id == id);

    match entry {
        Some(e) => render_template(&ctx.jinja_env, "snapshot.html", json!({ "entry": e })),
        None => (
            StatusCode::NOT_FOUND,
            Html("<h1>Snapshot Not Found</h1>".to_string()),
        ),
    }
}

async fn handle_export_pdf(
    State(ctx): State<AppContext>,
    AxumPath(id): AxumPath<i64>,
) -> impl IntoResponse {
    let entries = ctx.cache.get_all();
    let entry = entries.into_iter().find(|e| e.id == id);

    match entry {
        Some(e) => render_template(&ctx.jinja_env, "export_pdf.html", json!({ "entry": e })),
        None => (
            StatusCode::NOT_FOUND,
            Html("<h1>Snapshot Not Found</h1>".to_string()),
        ),
    }
}

async fn handle_update_note(
    State(ctx): State<AppContext>,
    AxumPath(id): AxumPath<i64>,
    Json(payload): Json<NotesRequest>,
) -> impl IntoResponse {
    handle_api_notes(State(ctx), AxumPath(id), Json(payload)).await
}

async fn handle_delete_single(
    State(ctx): State<AppContext>,
    AxumPath(id): AxumPath<i64>,
) -> impl IntoResponse {
    let entries = ctx.cache.get_all();
    if let Some(entry) = entries.iter().find(|e| e.id == id) {
        if !entry.filename.is_empty() {
            let file_path = Path::new(&ctx.screenshots_dir).join(&entry.filename);
            if file_path.exists() {
                let _ = std::fs::remove_file(file_path);
            }
        }
    }

    match ctx.db.delete_entry(id) {
        Ok(_) => {
            ctx.cache.remove(id);
            (StatusCode::OK, Json(json!({ "status": "success" })))
        }
        Err(e) => {
            error!("Error deleting entry: {}", e);
            (
                StatusCode::INTERNAL_SERVER_ERROR,
                Json(json!({ "status": "error" })),
            )
        }
    }
}

async fn handle_bulk_delete(
    State(ctx): State<AppContext>,
    Form(payload): Form<BulkDeleteForm>,
) -> impl IntoResponse {
    let current_time = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map(|d| d.as_secs() as i64)
        .unwrap_or(0);

    let range_secs = (payload.range * 3600) as i64;
    let start_timestamp = current_time - range_secs;
    let end_timestamp = current_time;

    let _ = ctx
        .db
        .delete_entries_by_range(start_timestamp, end_timestamp, &ctx.screenshots_dir);
    ctx.cache.remove_by_range(start_timestamp, end_timestamp);

    Redirect::to("/dashboard")
}

async fn handle_purge(State(ctx): State<AppContext>) -> impl IntoResponse {
    let _ = ctx.db.purge_all(&ctx.screenshots_dir);
    ctx.cache.clear_all();

    Redirect::to("/dashboard")
}

async fn handle_api_purge(State(ctx): State<AppContext>) -> impl IntoResponse {
    match ctx.db.purge_all(&ctx.screenshots_dir) {
        Ok(count) => {
            ctx.cache.clear_all();
            Json(json!({ "status": "success", "purged": count }))
        }
        Err(e) => {
            error!("Error purging all data: {}", e);
            Json(json!({ "status": "error" }))
        }
    }
}

async fn handle_api_heatmap(State(ctx): State<AppContext>) -> impl IntoResponse {
    match ctx.db.get_heatmap_data() {
        Ok(data) => Json(json!(data)),
        Err(e) => {
            error!("Error getting heatmap data: {}", e);
            Json(json!({}))
        }
    }
}

async fn handle_api_wordcloud(State(ctx): State<AppContext>) -> impl IntoResponse {
    match ctx.db.get_wordcloud_data() {
        Ok(data) => {
            let result: Vec<_> = data
                .into_iter()
                .map(|(text, size)| json!({ "text": text, "size": size }))
                .collect();
            Json(json!(result))
        }
        Err(e) => {
            error!("Error getting wordcloud data: {}", e);
            Json(json!([]))
        }
    }
}

async fn handle_api_dashboard(State(ctx): State<AppContext>) -> impl IntoResponse {
    let entries = ctx.cache.get_all();
    let total_snapshots = entries.len();

    let mut app_counts: HashMap<String, usize> = HashMap::new();
    for entry in &entries {
        *app_counts.entry(entry.app.clone()).or_insert(0) += 1;
    }

    let favorites_count = entries.iter().filter(|e| e.is_favorite).count();

    Json(json!({
        "total_snapshots": total_snapshots,
        "favorites_count": favorites_count,
        "app_distribution": app_counts,
        "is_paused": ctx.state.is_recording_paused(),
    }))
}

async fn handle_api_timeline(State(ctx): State<AppContext>) -> impl IntoResponse {
    let entries = ctx.cache.get_all();
    let timeline_data: Vec<_> = entries
        .into_iter()
        .map(|e| {
            json!({
                "id": e.id,
                "timestamp": e.timestamp,
                "app": e.app,
                "title": e.title,
                "filename": e.filename,
                "notes": e.notes,
                "is_favorite": e.is_favorite,
            })
        })
        .collect();

    Json(json!({ "entries": timeline_data }))
}

async fn handle_api_search(
    State(ctx): State<AppContext>,
    Query(query): Query<SearchQuery>,
) -> impl IntoResponse {
    let q = query.q.unwrap_or_default();
    let entries = ctx.cache.get_all();

    if q.trim().is_empty() {
        return Json(json!({ "results": [] }));
    }

    let query_embedding = ctx.ml_engine.generate_embedding(&q);
    let mut scored_entries = Vec::new();

    for entry in entries {
        let score = if !entry.embedding.is_empty() {
            cosine_similarity(&query_embedding, &entry.embedding)
        } else {
            0.0
        };

        let text_match = entry.text.to_lowercase().contains(&q.to_lowercase())
            || entry.app.to_lowercase().contains(&q.to_lowercase())
            || entry.title.to_lowercase().contains(&q.to_lowercase());

        if score > 0.3 || text_match {
            scored_entries.push((entry, score));
        }
    }

    scored_entries.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));

    let results: Vec<_> = scored_entries
        .into_iter()
        .map(|(e, score)| {
            json!({
                "id": e.id,
                "timestamp": e.timestamp,
                "app": e.app,
                "title": e.title,
                "text": e.text,
                "filename": e.filename,
                "notes": e.notes,
                "is_favorite": e.is_favorite,
                "score": score,
            })
        })
        .collect();

    Json(json!({ "results": results }))
}

async fn handle_api_settings(
    State(ctx): State<AppContext>,
    Json(payload): Json<SettingsRequest>,
) -> impl IntoResponse {
    if let Some(paused) = payload.recording_paused {
        ctx.state.set_recording_paused(paused);
    }

    Json(json!({
        "status": "success",
        "recording_paused": ctx.state.is_recording_paused()
    }))
}

async fn handle_api_notes(
    State(ctx): State<AppContext>,
    AxumPath(id): AxumPath<i64>,
    Json(payload): Json<NotesRequest>,
) -> impl IntoResponse {
    match ctx.db.update_entry_notes(id, &payload.notes) {
        Ok(true) => {
            ctx.cache.update_notes(id, &payload.notes);
            Json(json!({ "status": "success" }))
        }
        Ok(false) => Json(json!({ "status": "not_found" })),
        Err(e) => {
            error!("Error updating notes: {}", e);
            Json(json!({ "status": "error" }))
        }
    }
}

async fn handle_api_favorite(
    State(ctx): State<AppContext>,
    AxumPath(id): AxumPath<i64>,
) -> impl IntoResponse {
    match ctx.db.toggle_favorite(id) {
        Ok(true) => {
            ctx.cache.toggle_favorite(id);
            Json(json!({ "status": "success" }))
        }
        Ok(false) => Json(json!({ "status": "not_found" })),
        Err(e) => {
            error!("Error toggling favorite: {}", e);
            Json(json!({ "status": "error" }))
        }
    }
}

async fn handle_api_delete_range(
    State(ctx): State<AppContext>,
    Json(payload): Json<DeleteRangeRequest>,
) -> impl IntoResponse {
    match ctx.db.delete_entries_by_range(
        payload.start_timestamp,
        payload.end_timestamp,
        &ctx.screenshots_dir,
    ) {
        Ok(count) => {
            ctx.cache
                .remove_by_range(payload.start_timestamp, payload.end_timestamp);
            Json(json!({ "status": "success", "deleted": count }))
        }
        Err(e) => {
            error!("Error deleting entries by range: {}", e);
            Json(json!({ "status": "error" }))
        }
    }
}

async fn handle_api_delete_app(
    State(ctx): State<AppContext>,
    Json(payload): Json<DeleteAppRequest>,
) -> impl IntoResponse {
    match ctx
        .db
        .delete_entries_by_app(&payload.app_name, &ctx.screenshots_dir)
    {
        Ok(count) => {
            ctx.cache.remove_by_app(&payload.app_name);
            Json(json!({ "status": "success", "deleted": count }))
        }
        Err(e) => {
            error!("Error deleting entries by app: {}", e);
            Json(json!({ "status": "error" }))
        }
    }
}

fn render_template(
    env: &Environment<'static>,
    template_name: &str,
    ctx: serde_json::Value,
) -> (StatusCode, Html<String>) {
    match env.get_template(template_name) {
        Ok(tmpl) => match tmpl.render(ctx) {
            Ok(content) => (StatusCode::OK, Html(content)),
            Err(e) => (
                StatusCode::INTERNAL_SERVER_ERROR,
                Html(format!("<h1>Template Render Error: {}</h1>", e)),
            ),
        },
        Err(e) => (
            StatusCode::NOT_FOUND,
            Html(format!("<h1>Template Not Found: {}</h1>", e)),
        ),
    }
}
