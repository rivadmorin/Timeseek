use rusqlite::{params, Connection, Result, Row};
use serde::{Deserialize, Serialize};
use std::path::Path;
use std::time::{SystemTime, UNIX_EPOCH};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Entry {
    pub id: i64,
    pub app: String,
    pub title: String,
    pub text: String,
    pub timestamp: i64,
    pub embedding: Vec<f32>,
    pub filename: String,
    pub notes: String,
    pub is_favorite: bool,
}

pub struct NewEntry<'a> {
    pub text: &'a str,
    pub timestamp: i64,
    pub embedding: &'a [f32],
    pub app: &'a str,
    pub title: &'a str,
    pub filename: &'a str,
    pub notes: &'a str,
    pub is_favorite: bool,
}

pub struct Database {
    db_path: String,
}

impl Database {
    pub fn new(db_path: &str) -> Result<Self> {
        let db = Database {
            db_path: db_path.to_string(),
        };
        db.init()?;
        Ok(db)
    }

    fn get_conn(&self) -> Result<Connection> {
        Connection::open(&self.db_path)
    }

    pub fn init(&self) -> Result<()> {
        let conn = self.get_conn()?;

        conn.execute(
            "CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                app TEXT,
                title TEXT,
                text TEXT,
                timestamp INTEGER UNIQUE,
                embedding BLOB
            )",
            [],
        )?;

        // Schema Migrations: add columns if not present
        let mut stmt = conn.prepare("PRAGMA table_info(entries)")?;
        let columns: Vec<String> = stmt
            .query_map([], |row| row.get::<_, String>(1))?
            .filter_map(|r| r.ok())
            .collect();

        if !columns.contains(&"filename".to_string()) {
            conn.execute("ALTER TABLE entries ADD COLUMN filename TEXT", [])?;
        }

        if !columns.contains(&"notes".to_string()) {
            conn.execute("ALTER TABLE entries ADD COLUMN notes TEXT DEFAULT ''", [])?;
        }

        if !columns.contains(&"is_favorite".to_string()) {
            conn.execute(
                "ALTER TABLE entries ADD COLUMN is_favorite INTEGER DEFAULT 0",
                [],
            )?;
        }

        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_timestamp ON entries (timestamp)",
            [],
        )?;

        Ok(())
    }

    fn parse_row(row: &Row) -> Result<Entry> {
        let id: i64 = row.get(0)?;
        let app: Option<String> = row.get(1)?;
        let title: Option<String> = row.get(2)?;
        let text: Option<String> = row.get(3)?;
        let timestamp: i64 = row.get(4)?;
        let embedding_blob: Option<Vec<u8>> = row.get(5)?;
        let filename: Option<String> = row.get(6)?;
        let notes: Option<String> = row.get(7)?;
        let is_favorite: Option<i64> = row.get(8)?;

        let embedding = match embedding_blob {
            Some(bytes) => bytes
                .chunks_exact(4)
                .map(|chunk| f32::from_le_bytes(chunk.try_into().unwrap_or([0; 4])))
                .collect(),
            None => Vec::new(),
        };

        Ok(Entry {
            id,
            app: app.unwrap_or_default(),
            title: title.unwrap_or_default(),
            text: text.unwrap_or_default(),
            timestamp,
            embedding,
            filename: filename.unwrap_or_default(),
            notes: notes.unwrap_or_default(),
            is_favorite: is_favorite.unwrap_or(0) == 1,
        })
    }

    pub fn get_all_entries(&self) -> Result<Vec<Entry>> {
        let conn = self.get_conn()?;
        let mut stmt = conn.prepare(
            "SELECT id, app, title, text, timestamp, embedding, filename, notes, is_favorite
             FROM entries ORDER BY timestamp DESC",
        )?;

        let rows = stmt.query_map([], Self::parse_row)?;
        let mut entries = Vec::new();
        for entry in rows {
            entries.push(entry?);
        }
        Ok(entries)
    }

    pub fn insert_entry(&self, new_entry: NewEntry) -> Result<Option<i64>> {
        let conn = self.get_conn()?;
        let embedding_bytes: Vec<u8> = new_entry
            .embedding
            .iter()
            .flat_map(|f| f.to_le_bytes().to_vec())
            .collect();

        let updated_rows = conn.execute(
            "INSERT INTO entries (text, timestamp, embedding, app, title, filename, notes, is_favorite)
             VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8)
             ON CONFLICT(timestamp) DO NOTHING",
            params![
                new_entry.text,
                new_entry.timestamp,
                embedding_bytes,
                new_entry.app,
                new_entry.title,
                new_entry.filename,
                new_entry.notes,
                if new_entry.is_favorite { 1 } else { 0 }
            ],
        )?;

        if updated_rows > 0 {
            Ok(Some(conn.last_insert_rowid()))
        } else {
            Ok(None)
        }
    }

    pub fn toggle_favorite(&self, entry_id: i64) -> Result<bool> {
        let conn = self.get_conn()?;
        let updated = conn.execute(
            "UPDATE entries SET is_favorite = CASE WHEN is_favorite = 1 THEN 0 ELSE 1 END WHERE id = ?1",
            params![entry_id],
        )?;
        Ok(updated > 0)
    }

    pub fn update_entry_notes(&self, entry_id: i64, notes: &str) -> Result<bool> {
        let conn = self.get_conn()?;
        let updated = conn.execute(
            "UPDATE entries SET notes = ?1 WHERE id = ?2",
            params![notes, entry_id],
        )?;
        Ok(updated > 0)
    }

    pub fn delete_entry(&self, entry_id: i64) -> Result<bool> {
        let conn = self.get_conn()?;
        let updated = conn.execute("DELETE FROM entries WHERE id = ?1", params![entry_id])?;
        Ok(updated > 0)
    }

    pub fn prune_old_data(&self, retention_days: u64, screenshots_dir: &str) -> Result<usize> {
        let current_time = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map(|d| d.as_secs() as i64)
            .unwrap_or(0);
        let cutoff_timestamp = current_time - (retention_days as i64 * 86400);

        let conn = self.get_conn()?;
        let mut stmt = conn.prepare("SELECT filename FROM entries WHERE timestamp < ?1")?;
        let filenames: Vec<String> = stmt
            .query_map(params![cutoff_timestamp], |row| {
                row.get::<_, Option<String>>(0)
            })?
            .filter_map(|r| r.ok().flatten())
            .collect();

        for filename in filenames {
            if !filename.is_empty() {
                let file_path = Path::new(screenshots_dir).join(&filename);
                if file_path.exists() {
                    let _ = std::fs::remove_file(file_path);
                }
            }
        }

        let deleted_count = conn.execute(
            "DELETE FROM entries WHERE timestamp < ?1",
            params![cutoff_timestamp],
        )?;

        Ok(deleted_count)
    }

    pub fn delete_entries_by_range(
        &self,
        start: i64,
        end: i64,
        screenshots_dir: &str,
    ) -> Result<usize> {
        let conn = self.get_conn()?;
        let mut stmt =
            conn.prepare("SELECT filename FROM entries WHERE timestamp >= ?1 AND timestamp <= ?2")?;
        let filenames: Vec<String> = stmt
            .query_map(params![start, end], |row| row.get::<_, Option<String>>(0))?
            .filter_map(|r| r.ok().flatten())
            .collect();

        for filename in filenames {
            if !filename.is_empty() {
                let file_path = Path::new(screenshots_dir).join(&filename);
                if file_path.exists() {
                    let _ = std::fs::remove_file(file_path);
                }
            }
        }

        let deleted_count = conn.execute(
            "DELETE FROM entries WHERE timestamp >= ?1 AND timestamp <= ?2",
            params![start, end],
        )?;

        Ok(deleted_count)
    }

    pub fn delete_entries_by_app(&self, app_name: &str, screenshots_dir: &str) -> Result<usize> {
        let conn = self.get_conn()?;
        let mut stmt = conn.prepare("SELECT filename FROM entries WHERE app = ?1")?;
        let filenames: Vec<String> = stmt
            .query_map(params![app_name], |row| row.get::<_, Option<String>>(0))?
            .filter_map(|r| r.ok().flatten())
            .collect();

        for filename in filenames {
            if !filename.is_empty() {
                let file_path = Path::new(screenshots_dir).join(&filename);
                if file_path.exists() {
                    let _ = std::fs::remove_file(file_path);
                }
            }
        }

        let deleted_count =
            conn.execute("DELETE FROM entries WHERE app = ?1", params![app_name])?;

        Ok(deleted_count)
    }

    pub fn purge_all(&self, screenshots_dir: &str) -> Result<usize> {
        let conn = self.get_conn()?;
        let mut stmt = conn.prepare("SELECT filename FROM entries")?;
        let filenames: Vec<String> = stmt
            .query_map([], |row| row.get::<_, Option<String>>(0))?
            .filter_map(|r| r.ok().flatten())
            .collect();

        for filename in filenames {
            if !filename.is_empty() {
                let file_path = Path::new(screenshots_dir).join(&filename);
                if file_path.exists() {
                    let _ = std::fs::remove_file(file_path);
                }
            }
        }

        let deleted_count = conn.execute("DELETE FROM entries", [])?;
        Ok(deleted_count)
    }

    pub fn get_heatmap_data(&self) -> Result<std::collections::HashMap<String, usize>> {
        let entries = self.get_all_entries()?;
        let mut heatmap = std::collections::HashMap::new();

        for entry in entries {
            if entry.timestamp > 0 {
                if let Some(datetime) = chrono::DateTime::from_timestamp(entry.timestamp, 0) {
                    let date_str = datetime.format("%Y-%m-%d").to_string();
                    *heatmap.entry(date_str).or_insert(0) += 1;
                }
            }
        }

        Ok(heatmap)
    }

    pub fn get_wordcloud_data(&self) -> Result<Vec<(String, usize)>> {
        let entries = self.get_all_entries()?;
        let mut counts = std::collections::HashMap::new();

        let stop_words: std::collections::HashSet<&str> = [
            "the", "be", "to", "of", "and", "a", "in", "that", "have", "i",
            "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
            "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
            "or", "an", "will", "my", "one", "all", "would", "there", "their", "what",
            "so", "up", "out", "if", "about", "who", "get", "which", "go", "me",
            "is", "are", "was", "were", "been", "has", "had", "http", "https", "com",
        ].iter().cloned().collect();

        for entry in entries {
            let combined_text = format!("{} {} {}", entry.title, entry.text, entry.notes);
            for word in combined_text.split_whitespace() {
                let cleaned: String = word
                    .chars()
                    .filter(|c| c.is_alphanumeric())
                    .collect::<String>()
                    .to_lowercase();

                if cleaned.len() > 2 && !stop_words.contains(cleaned.as_str()) {
                    *counts.entry(cleaned).or_insert(0) += 1;
                }
            }
        }

        let mut sorted_counts: Vec<(String, usize)> = counts.into_iter().collect();
        sorted_counts.sort_by(|a, b| b.1.cmp(&a.1));
        sorted_counts.truncate(50);

        Ok(sorted_counts)
    }
}
