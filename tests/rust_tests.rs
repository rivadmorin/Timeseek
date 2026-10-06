use tempfile::NamedTempFile;
use timeseek::db::{Database, NewEntry};
use timeseek::ml::cosine_similarity;
use timeseek::state::AppState;

#[test]
fn test_state_pause_toggle() {
    let state = AppState::new();
    assert!(!state.is_recording_paused());
    state.set_recording_paused(true);
    assert!(state.is_recording_paused());
    state.set_recording_paused(false);
    assert!(!state.is_recording_paused());
}

#[test]
fn test_db_crud() {
    let tmp_file = NamedTempFile::new().unwrap();
    let db_path = tmp_file.path().to_str().unwrap();

    let db = Database::new(db_path).unwrap();

    let embedding = vec![0.1f32; 384];
    let new_entry = NewEntry {
        text: "Test screenshot content",
        timestamp: 1000000,
        embedding: &embedding,
        app: "Firefox",
        title: "Mozilla Firefox",
        filename: "1000000.jpg",
        notes: "Initial Note",
        is_favorite: false,
    };

    let inserted_id = db.insert_entry(new_entry).unwrap();

    assert!(inserted_id.is_some());
    let id = inserted_id.unwrap();

    let entries = db.get_all_entries().unwrap();
    assert_eq!(entries.len(), 1);
    assert_eq!(entries[0].app, "Firefox");
    assert_eq!(entries[0].notes, "Initial Note");

    let toggled = db.toggle_favorite(id).unwrap();
    assert!(toggled);

    let entries = db.get_all_entries().unwrap();
    assert!(entries[0].is_favorite);

    let updated = db.update_entry_notes(id, "Updated Note").unwrap();
    assert!(updated);

    let entries = db.get_all_entries().unwrap();
    assert_eq!(entries[0].notes, "Updated Note");

    let deleted = db.delete_entry(id).unwrap();
    assert!(deleted);

    let entries = db.get_all_entries().unwrap();
    assert_eq!(entries.len(), 0);
}

#[test]
fn test_cosine_similarity() {
    let v1 = vec![1.0, 0.0, 0.0];
    let v2 = vec![1.0, 0.0, 0.0];
    let sim = cosine_similarity(&v1, &v2);
    assert!((sim - 1.0).abs() < 1e-5);

    let v3 = vec![0.0, 1.0, 0.0];
    let sim_orthogonal = cosine_similarity(&v1, &v3);
    assert!((sim_orthogonal - 0.0).abs() < 1e-5);
}
