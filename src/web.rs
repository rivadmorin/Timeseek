use crate::cache::EntryCache;
use crate::db::Database;
use crate::ml::{cosine_similarity, VectorEmbeddingEngine};
use crate::state::AppState;
use axum::{
    extract::{Path as AxumPath, Query, State},
    http::StatusCode,
    response::{Html, IntoResponse},
    routing::{get, post},
    Json, Router,
};
use minijinja::Environment;
use serde::Deserialize;
use serde_json::json;
use std::collections::HashMap;
use std::sync::Arc;
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
        .route("/timeline", get(handle_timeline))
        .route("/search", get(handle_search_page))
        .route("/settings", get(handle_settings_page))
        .route("/snapshot/:id", get(handle_snapshot_detail))
        .route("/api/dashboard", get(handle_api_dashboard))
        .route("/api/timeline", get(handle_api_timeline))
        .route("/api/search", get(handle_api_search))
        .route("/api/settings", post(handle_api_settings))
        .route("/api/entries/:id/notes", post(handle_api_notes))
        .route("/api/entries/:id/favorite", post(handle_api_favorite))
        .route("/api/delete_range", post(handle_api_delete_range))
        .route("/api/delete_app", post(handle_api_delete_app))
        .nest_service("/static", ServeDir::new("timeseek/static"))
        .nest_service("/screenshots", ServeDir::new(&ctx.screenshots_dir))
        .with_state(ctx)
}

async fn handle_index(State(ctx): State<AppContext>) -> impl IntoResponse {
    render_template(&ctx.jinja_env, "dashboard.html", json!({}))
}

async fn handle_timeline(State(ctx): State<AppContext>) -> impl IntoResponse {
    render_template(&ctx.jinja_env, "timeline.html", json!({}))
}

async fn handle_search_page(State(ctx): State<AppContext>) -> impl IntoResponse {
    render_template(&ctx.jinja_env, "search.html", json!({}))
}

async fn handle_settings_page(State(ctx): State<AppContext>) -> impl IntoResponse {
    render_template(&ctx.jinja_env, "settings.html", json!({}))
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
