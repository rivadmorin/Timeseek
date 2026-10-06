use std::sync::atomic::{AtomicBool, Ordering};

pub struct AppState {
    recording_paused: AtomicBool,
}

impl AppState {
    pub fn new() -> Self {
        AppState {
            recording_paused: AtomicBool::new(false),
        }
    }

    pub fn is_recording_paused(&self) -> bool {
        self.recording_paused.load(Ordering::SeqCst)
    }

    pub fn set_recording_paused(&self, paused: bool) {
        self.recording_paused.store(paused, Ordering::SeqCst);
    }
}

impl Default for AppState {
    fn default() -> Self {
        Self::new()
    }
}
