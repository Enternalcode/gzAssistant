import json
import hnswlib
from typing import List, Tuple
import numpy as np
from apps.services.slm.slm_service import SlmService
from apps.utils.config import APPLICATION_DATA_PATH


class HnswlibVectorDB:
    def __init__(self, ai_service: SlmService):
        self.ai_service = ai_service
        self.index = None
        self.texts = []
        self.persistence_path = f"{APPLICATION_DATA_PATH}/embedding"
        self.dim = self._dim()

    def _dim(self) -> int:
        sample_vector = self.ai_service.embeddings_sync("hello")
        print(f"sample_vector: {len(sample_vector)}")
        return len(sample_vector)

    def initialize_index(self, max_elements: int):
        self.index = hnswlib.Index(space='cosine', dim=self.dim)
        self.index.init_index(max_elements=max_elements, ef_construction=200, M=16)

    def add_text(self, text: str):
        vectors = self.ai_service.embeddings_sync(text)
        self.texts.append(text)
        current_index = len(self.texts) - 1  # 获取当前文本的索引
        self.index.add_items(vectors, ids=np.array([current_index]))  # 使用当前索引作为 ID

    def search(self, query: str, k: int = 5) -> List[Tuple[str, float]]:
        query_vector = self.ai_service.embeddings_sync(query)
        labels, distances = self.index.knn_query(query_vector, k=k)
        results = [(self.texts[label], 1 - distances[0][i]) for i, label in enumerate(labels[0])]
        return [(text, round(score, 2)) for text, score in results]

    def save(self, index_path: str = "index.bin", texts_path: str = "texts.json" ):
        index_path = f'{self.persistence_path}/{index_path}'
        texts_path = f'{self.persistence_path}/{texts_path}'
        self.index.save_index(index_path)
        with open(texts_path, 'w', encoding='utf-8') as f:
            json.dump(self.texts, f, ensure_ascii=False)

    def load(self, index_path: str = "index.bin", texts_path: str = "texts.json" ):
        index_path = f'{self.persistence_path}/{index_path}'
        texts_path = f'{self.persistence_path}/{texts_path}'
        with open(texts_path, 'r', encoding='utf-8') as f:
            self.texts = json.load(f)
        self.index = hnswlib.Index(space='cosine', dim=self.dim)
        self.index.load_index(index_path, max_elements=len(self.texts))