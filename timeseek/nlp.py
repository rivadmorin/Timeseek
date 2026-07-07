import numpy as np
from sentence_transformers import SentenceTransformer
import logging
from functools import lru_cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
MODEL_NAME: str = "all-MiniLM-L6-v2"
EMBEDDING_DIM: int = 384  # Dimension for all-MiniLM-L6-v2

# Load the model globally to avoid reloading it on every call
try:
    model = SentenceTransformer(MODEL_NAME)
    logger.info(f"SentenceTransformer model '{MODEL_NAME}' loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load SentenceTransformer model '{MODEL_NAME}': {e}")
    model = None


@lru_cache(maxsize=128)
def get_embedding(text: str) -> np.ndarray:
    """
    Generates a sentence embedding for the given text.
    Added LRU cache to avoid redundant embedding calculations for similar queries.
    """
    if model is None:
        logger.error("SentenceTransformer model is not loaded. Returning zero vector.")
        return np.zeros(EMBEDDING_DIM, dtype=np.float32)

    if not text or text.isspace():
        logger.warning("Input text is empty or whitespace. Returning zero vector.")
        return np.zeros(EMBEDDING_DIM, dtype=np.float32)

    sentences = [line for line in text.split("\n") if line.strip()]

    if not sentences:
        logger.warning("No non-empty lines found after splitting. Returning zero vector.")
        return np.zeros(EMBEDDING_DIM, dtype=np.float32)

    try:
        # Optimization: encode all sentences in a single batch
        sentence_embeddings = model.encode(sentences, show_progress_bar=False)
        mean_embedding = np.mean(sentence_embeddings, axis=0, dtype=np.float32)
        return mean_embedding
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        return np.zeros(EMBEDDING_DIM, dtype=np.float32)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Calculates cosine similarity using optimized numpy operations."""
    # Ensure they are float32 for consistency
    a = a.astype(np.float32)
    b = b.astype(np.float32)

    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    similarity = np.dot(a, b) / (norm_a * norm_b)
    return float(np.clip(similarity, -1.0, 1.0))

def batch_cosine_similarity(query_embedding: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    """Calculates cosine similarity for a query against a matrix of embeddings."""
    # Matrix shape: (N, EMBEDDING_DIM)
    query_norm = np.linalg.norm(query_embedding)
    matrix_norms = np.linalg.norm(matrix, axis=1)

    if query_norm == 0:
        return np.zeros(matrix.shape[0])

    # Avoid division by zero
    matrix_norms[matrix_norms == 0] = 1.0

    dot_products = np.dot(matrix, query_embedding)
    similarities = dot_products / (query_norm * matrix_norms)
    return np.clip(similarities, -1.0, 1.0)
