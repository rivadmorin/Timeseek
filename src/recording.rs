use crate::cache::EntryCache;
use crate::db::{Database, Entry, NewEntry};
use crate::image_proc::calculate_ssim;
use crate::state::AppState;
use image::{DynamicImage, RgbaImage};
use screenshots::Screen;
use std::fs;
use std::path::Path;
use std::sync::Arc;
use std::time::{Duration, SystemTime, UNIX_EPOCH};
use tokio::time::sleep;
use tracing::{error, info};

pub struct RecorderConfig {
    pub screenshots_dir: String,
    pub db_path: String,
    pub blacklisted_apps: Vec<String>,
    pub blacklisted_keywords: Vec<String>,
    pub primary_monitor_only: bool,
    pub image_quality: u8,
}

pub struct ScreenRecorder {
    config: RecorderConfig,
    state: Arc<AppState>,
    db: Arc<Database>,
    cache: EntryCache,
}

impl ScreenRecorder {
    pub fn new(
        config: RecorderConfig,
        state: Arc<AppState>,
        db: Arc<Database>,
        cache: EntryCache,
    ) -> Self {
        ScreenRecorder {
            config,
            state,
            db,
            cache,
        }
    }

    pub async fn run_loop(self: Arc<Self>) {
        info!("Starting background screen recording worker loop...");
        let mut last_image: Option<DynamicImage> = None;

        loop {
            sleep(Duration::from_secs(2)).await;

            if self.state.is_recording_paused() {
                continue;
            }

            let screens = match Screen::all() {
                Ok(screens) => screens,
                Err(err) => {
                    error!("Failed to enumerate screens: {}", err);
                    continue;
                }
            };

            if screens.is_empty() {
                continue;
            }

            let screen = if self.config.primary_monitor_only {
                screens
                    .iter()
                    .find(|s| s.display_info.is_primary)
                    .unwrap_or(&screens[0])
            } else {
                &screens[0]
            };

            let captured = match screen.capture() {
                Ok(img) => img,
                Err(e) => {
                    error!("Error capturing screen: {}", e);
                    continue;
                }
            };

            let width = captured.width();
            let height = captured.height();
            let raw_bytes = captured.into_raw();

            let rgba_buf = match RgbaImage::from_raw(width, height, raw_bytes) {
                Some(buf) => buf,
                None => continue,
            };

            let dynamic_img = DynamicImage::ImageRgba8(rgba_buf);

            // Deduplication via SSIM
            if let Some(ref prev_img) = last_image {
                let ssim = calculate_ssim(prev_img, &dynamic_img);
                if ssim > 0.98 {
                    // Frame unchanged, skip duplicate recording
                    continue;
                }
            }

            let timestamp = SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .map(|d| d.as_secs() as i64)
                .unwrap_or(0);

            let filename = format!("{}.jpg", timestamp);
            let file_path = Path::new(&self.config.screenshots_dir).join(&filename);

            if let Err(e) = fs::create_dir_all(&self.config.screenshots_dir) {
                error!("Failed to create screenshots directory: {}", e);
                continue;
            }

            let mut jpeg_bytes = Vec::new();
            let mut cursor = std::io::Cursor::new(&mut jpeg_bytes);
            if let Err(e) = dynamic_img.write_to(&mut cursor, image::ImageFormat::Jpeg) {
                error!("Failed to encode image to JPEG: {}", e);
                continue;
            }

            if let Err(e) = fs::write(&file_path, jpeg_bytes) {
                error!("Failed to save screenshot file: {}", e);
                continue;
            }

            last_image = Some(dynamic_img);

            // Placeholder metadata
            let app_name = "Desktop".to_string();
            let window_title = "Screen Capture".to_string();
            let extracted_text = "".to_string();
            let dummy_embedding = vec![0.0f32; 384];

            // Blacklist check
            let lower_app = app_name.to_lowercase();
            if self
                .config
                .blacklisted_apps
                .iter()
                .any(|b| lower_app.contains(&b.to_lowercase()))
            {
                continue;
            }

            let lower_text = extracted_text.to_lowercase();
            if self
                .config
                .blacklisted_keywords
                .iter()
                .any(|k| !k.is_empty() && lower_text.contains(&k.to_lowercase()))
            {
                continue;
            }

            let new_entry = NewEntry {
                text: &extracted_text,
                timestamp,
                embedding: &dummy_embedding,
                app: &app_name,
                title: &window_title,
                filename: &filename,
                notes: "",
                is_favorite: false,
            };

            match self.db.insert_entry(new_entry) {
                Ok(Some(id)) => {
                    let entry = Entry {
                        id,
                        app: app_name,
                        title: window_title,
                        text: extracted_text,
                        timestamp,
                        embedding: dummy_embedding,
                        filename,
                        notes: String::new(),
                        is_favorite: false,
                    };
                    self.cache.add(entry);
                }
                Ok(None) => {}
                Err(e) => error!("Failed to insert screenshot record: {}", e),
            }
        }
    }
}
