use crate::db::Entry;
use std::sync::{Arc, RwLock};

#[derive(Clone)]
pub struct EntryCache {
    entries: Arc<RwLock<Vec<Entry>>>,
}

impl EntryCache {
    pub fn new() -> Self {
        EntryCache {
            entries: Arc::new(RwLock::new(Vec::new())),
        }
    }

    pub fn set(&self, entries: Vec<Entry>) {
        if let Ok(mut lock) = self.entries.write() {
            *lock = entries;
        }
    }

    pub fn get_all(&self) -> Vec<Entry> {
        if let Ok(lock) = self.entries.read() {
            lock.clone()
        } else {
            Vec::new()
        }
    }

    pub fn add(&self, entry: Entry) {
        if let Ok(mut lock) = self.entries.write() {
            lock.insert(0, entry);
        }
    }

    pub fn update_notes(&self, entry_id: i64, notes: &str) {
        if let Ok(mut lock) = self.entries.write() {
            if let Some(entry) = lock.iter_mut().find(|e| e.id == entry_id) {
                entry.notes = notes.to_string();
            }
        }
    }

    pub fn toggle_favorite(&self, entry_id: i64) {
        if let Ok(mut lock) = self.entries.write() {
            if let Some(entry) = lock.iter_mut().find(|e| e.id == entry_id) {
                entry.is_favorite = !entry.is_favorite;
            }
        }
    }

    pub fn remove(&self, entry_id: i64) {
        if let Ok(mut lock) = self.entries.write() {
            lock.retain(|e| e.id != entry_id);
        }
    }

    pub fn remove_by_range(&self, start: i64, end: i64) {
        if let Ok(mut lock) = self.entries.write() {
            lock.retain(|e| e.timestamp < start || e.timestamp > end);
        }
    }

    pub fn remove_by_app(&self, app_name: &str) {
        if let Ok(mut lock) = self.entries.write() {
            lock.retain(|e| e.app != app_name);
        }
    }
}

impl Default for EntryCache {
    fn default() -> Self {
        Self::new()
    }
}
