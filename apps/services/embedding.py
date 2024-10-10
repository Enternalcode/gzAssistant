from utils import default_config
from llama_cpp import Llama

class EmbeddingModel:
    instance = None

    @staticmethod
    def get_model():
        if EmbeddingModel.instance is None:
            model_path = default_config['EMBEDDING_MODEL_PATH']
            EmbeddingModel.instance  = Llama(model_path=model_path, embedding=True, verbose=False)
        return EmbeddingModel.instance
