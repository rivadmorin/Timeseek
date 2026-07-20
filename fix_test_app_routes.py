import re

with open('tests/test_app_routes.py', 'r') as f:
    content = f.read()

# The error happens because the embedding is shape (3,) but the model outputs (384,).
# So let's create a dummy (384,) array for embedding.
content = content.replace("embedding=np.array([1, 2, 3])", "embedding=np.zeros(384)")

with open('tests/test_app_routes.py', 'w') as f:
    f.write(content)
