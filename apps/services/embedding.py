from llama_cpp import Llama
from apps.utils.config import get_config

class EmbeddingModel:
    instance = None

    @staticmethod
    def get_model():
        if EmbeddingModel.instance is None:
            model_path = get_config('EMBEDDING_MODEL_PATH')
            EmbeddingModel.instance  = Llama(model_path=model_path, embedding=True, verbose=False)
        return EmbeddingModel.instance
