import numpy as np

class InMemoryVectorStore:
    def __init__(self):
        self.vectors = []
        self.metadata = []

    def add(self, embedding, metadata):
        self.vectors.append(np.array(embedding))
        self.metadata.append(metadata)

    def search(self, query_embedding, top_k=3):
        query = np.array(query_embedding)
        scores = []

        for i, vector in enumerate(self.vectors):
            score = np.dot(query, vector) / (
                np.linalg.norm(query) * np.linalg.norm(vector)
            )
            scores.append((score, self.metadata[i]))

        scores.sort(reverse=True, key=lambda x: x[0])
        return scores[:top_k]