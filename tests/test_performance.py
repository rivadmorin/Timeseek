import numpy as np
import time
from timeseek.nlp import batch_cosine_similarity, cosine_similarity

def test_batch_cosine_similarity_accuracy():
    """Verify that batch similarity matches single similarity."""
    query = np.random.rand(384).astype(np.float32)
    matrix = np.random.rand(10, 384).astype(np.float32)

    batch_results = batch_cosine_similarity(query, matrix)

    for i in range(10):
        single_result = cosine_similarity(query, matrix[i])
        assert np.isclose(batch_results[i], single_result, atol=1e-5)

def test_batch_cosine_similarity_performance():
    """Verify that batch similarity is faster than linear scan for large N."""
    N = 1000
    query = np.random.rand(384).astype(np.float32)
    matrix = np.random.rand(N, 384).astype(np.float32)

    start = time.time()
    for i in range(N):
        cosine_similarity(query, matrix[i])
    linear_time = time.time() - start

    start = time.time()
    batch_cosine_similarity(query, matrix)
    batch_time = time.time() - start

    print(f"\nLinear: {linear_time:.4f}s, Batch: {batch_time:.4f}s")
    assert batch_time < linear_time
