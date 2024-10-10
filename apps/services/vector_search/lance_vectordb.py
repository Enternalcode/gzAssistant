# from typing import List, Optional, Union
# from lancedb.pydantic import LanceModel, Vector
# from lancedb.embeddings.registry import EmbeddingFunctionRegistry
# import lancedb
# import pyarrow as pa
# from functools import cached_property
# from lancedb.embeddings.base import TextEmbeddingFunction
# from services.embedding import EmbeddingModel
# import numpy as np
# from llama_cpp import Llama
# from loguru import logger
# import pandas as pd

# registry = EmbeddingFunctionRegistry.get_instance()

# @registry.register("LlamaCppBge")
# class LlamaCppBgeEmbeddings(TextEmbeddingFunction):

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self._ndims = None
    
#     @cached_property
#     def _embedding_model(self) -> Llama:
#         return EmbeddingModel.get_model()

#     def generate_embeddings(self, texts: List[str]) -> List[np.array]:
#         embed_result = self._embedding_model.create_embedding(list(texts))
#         embeddings = []
#         for item in embed_result["data"]:
#             embeddings.append(item['embedding'])
#         return embeddings

#     def ndims(self):
#         if self._ndims is None:
#             self._ndims = len(self.generate_embeddings(["guangzhi"])[0])
#         return self._ndims

# llama_cpp_func = registry.get("LlamaCppBge").create(max_retries=0)

# class TextModelSchema(LanceModel):
#     text: str = llama_cpp_func.SourceField()
#     vector: Vector(llama_cpp_func.ndims()) = llama_cpp_func.VectorField()

# class LanceVectorDB:
#     def __init__(self, uri: str = "apps/data/lancedb/vectordb") -> None:
#         self.uri = uri
#         self.async_db = None
#         self.embedding_model = EmbeddingModel.get_model()
    
#     async def connect(self) -> None:
#         try:
#             self.async_db = await lancedb.connect_async(self.uri)
#             if self.async_db is None:
#                 raise RuntimeError("Failed to connect to the database.")
#         except Exception as e:
#             logger.error(f"Error connecting to the database: {e}")
#             self.async_db = None
    
#     async def get_table(self, table_name: str, schema: Optional[Union[pa.Schema, LanceModel]] = None) -> lancedb.table.AsyncTable:
#         if schema is None:
#             schema = TextModelSchema
#         return await self.async_db.create_table(table_name, schema=schema, exist_ok=True)
    
#     async def drop_table(self, table_name: str) -> None:
#         return await self.async_db.drop_table(table_name)
    
#     async def insert(self, table_name: str, data: List[dict]) -> None:
#             table = await self.get_table(table_name)
#             await table.add(data)
        
#     def _vectorize_text(self, text: str) -> np.array:
#         return self.embedding_model.create_embedding([text])['data'][0]['embedding']
    
#     async def query(self, table_name: str, query_text: str, limit: int = 3) -> List[dict]:
#             table = await self.get_table(table_name)
#             query_embedding = self._vectorize_text(query_text)
#             results = await table.vector_search(query_embedding).limit(limit).to_pandas()
#             if '_distance' in results.columns:
#                 sorted_results = results.sort_values(by='_distance', ascending=True)
#                 selected_results = sorted_results[['text', '_distance']]
#             else:
#                 selected_results = pd.DataFrame(columns=['text', '_distance'])
#             return selected_results.to_dict('records')  # 将 DataFrame 转换为字典列表
    
#     def close(self) -> None:
#         if self.async_db and self.async_db.is_open():
#             self.async_db.close()
    
#     async def __aenter__(self):
#         await self.connect()
#         if not self.async_db:
#             raise RuntimeError("Database connection was not established.")
#         return self
    
#     async def __aexit__(self, exc_type, exc_val, exc_tb):
#         self.close()
    
#     async def to_pands(self, table_name: str):
#         table = await self.get_table(table_name)
#         return await table.to_pandas()


# async def test_lancedb():
#     async with VectorDB() as vectordb:
#         res = await vectordb.to_pands("test")
#         # await vectordb.insert("test", [
#         #     {"text": "你好"},
#         #     {"text": "任务1：基于端侧大模型推理框架，如llama.cpp、MNN、mlc-llm等（使用Arm CPU），结合如RAG、Agent等，实现具备一个基本功能的小程序"},
#         #     {"text": "任务2：从正常对话速度，实时从中抓取时间信息"}
#         # ])
#         query = "比赛可以使用哪些推理框架"
#         actual = await vectordb.query("test", query)
#         print(actual)

    