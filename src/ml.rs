use image::DynamicImage;

pub fn cosine_similarity(v1: &[f32], v2: &[f32]) -> f32 {
    if v1.len() != v2.len() || v1.is_empty() {
        return 0.0;
    }

    let mut dot_product = 0.0f32;
    let mut norm_a = 0.0f32;
    let mut norm_b = 0.0f32;

    for i in 0..v1.len() {
        dot_product += v1[i] * v2[i];
        norm_a += v1[i] * v1[i];
        norm_b += v2[i] * v2[i];
    }

    if norm_a == 0.0 || norm_b == 0.0 {
        return 0.0;
    }

    dot_product / (norm_a.sqrt() * norm_b.sqrt())
}

pub struct VectorEmbeddingEngine;

impl VectorEmbeddingEngine {
    pub fn new() -> Self {
        VectorEmbeddingEngine
    }

    pub fn generate_embedding(&self, text: &str) -> Vec<f32> {
        let mut embedding = vec![0.0f32; 384];
        if text.is_empty() {
            return embedding;
        }

        let bytes = text.as_bytes();
        for (i, &byte) in bytes.iter().enumerate() {
            let idx = i % 384;
            embedding[idx] += (byte as f32) / 255.0;
        }

        let norm: f32 = embedding.iter().map(|x| x * x).sum::<f32>().sqrt();
        if norm > 0.0 {
            for val in embedding.iter_mut() {
                *val /= norm;
            }
        }

        embedding
    }
}

impl Default for VectorEmbeddingEngine {
    fn default() -> Self {
        Self::new()
    }
}

pub struct OcrEngine;

impl OcrEngine {
    pub fn new() -> Self {
        OcrEngine
    }

    pub fn extract_text(&self, _img: &DynamicImage) -> String {
        String::new()
    }
}

impl Default for OcrEngine {
    fn default() -> Self {
        Self::new()
    }
}
