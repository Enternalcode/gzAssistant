import json
import hnswlib
from typing import List, Optional, Tuple
import numpy as np
from apps.services.slm.slm_service import SlmService
from apps.utils.config import APPLICATION_DATA_PATH


class HnswlibVectorDB:
    def __init__(self, ai_service: SlmService, fixed_dim: int = None):
        self.ai_service = ai_service
        self.index = None
        self.texts = []
        self.persistence_path = f"{APPLICATION_DATA_PATH}/embedding"
        if fixed_dim:
            self.dim = fixed_dim
        else:
            self.dim = self._dim()

    def _dim(self) -> int:
        sample_vector = self.ai_service.embeddings_sync("hello")
        print(f"len(sample_vector): {len(sample_vector)}")
        return len(sample_vector)

    def initialize_index(self, max_elements: int):
        self.index = hnswlib.Index(space='cosine', dim=self.dim)
        self.index.init_index(max_elements=max_elements, ef_construction=200, M=16)
        self.index.set_ef(10)
    
    def embed_texts(self, texts: List[str]) -> List[np.array]:
        cache = []
        for text in texts:
            vectors = self.ai_service.embeddings_sync(text)
            cache.append(vectors)
        return cache
    
    async def embed_texts_async(self, texts: List[str]) -> List[np.array]:
        cache = []
        for text in texts:
            vectors = await self.ai_service.embeddings_async(text)
            cache.append(vectors)
        return cache

    def add_texts(self, texts: List[str]):
        vectors = self.embed_texts(texts)
        self.texts.extend(texts)
        self.index.add_items(vectors, ids=np.arange(len(self.texts)))
    
    async def add_texts_async(self, texts: List[str]) -> None:
        vectors = await self.embed_texts_async(texts)
        self.texts.extend(texts)
        self.index.add_items(vectors, ids=np.arange(len(self.texts)))

    def search(self, query: str, k: int = 5, get_best: bool = True) -> Optional[Tuple[str, float]]:
        try:
            query_vector = self.ai_service.embeddings_sync(query)
            labels, distances = self.index.knn_query(query_vector, k=k)
            
            # 修改条件判断
            if not np.any(labels) or not np.any(distances):
                raise ValueError("No results returned from the index.")

            results = [(self.texts[label], distances[0][i]) for i, label in enumerate(labels[0])]
            
            if not results:
                raise ValueError("No results found for the given query.")
            
            sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
            
            if get_best:
                return sorted_results[0][0] if sorted_results else None
            else:
                return [(text, score) for text, score in sorted_results]
            
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    async def search_async(self, query: str, k: int = 5, get_best: bool = True, distance_threshold: float = 0.46) -> Optional[Tuple[str, float]] | list:
        try:
            query_vector = await self.ai_service.embeddings_async(query)
            labels, distances = self.index.knn_query(query_vector, k=k)

            if not np.any(labels) or not np.any(distances):
                raise ValueError("No results returned from the index.")

            results = [(self.texts[label], distances[0][i]) for i, label in enumerate(labels[0])]

            if not results:
                raise ValueError("No results found for the given query.")

            sorted_results = sorted(results, key=lambda x: x[1], reverse=False)
            filtered_results = [result for result in sorted_results if result[1] <= distance_threshold]

            if not filtered_results:
                return "", 1.0

            if get_best:
                return filtered_results[0]
            else:
                return filtered_results

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

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