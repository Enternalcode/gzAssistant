import openai
from typing import List, Dict

class SlmService:
    def __init__(self, base_url: str, api_key: str) -> None:
        """
        初始化 SlmService 类。

        :param base_url: API 服务器的基础 URL
        :param api_key: API 密钥
        """
        self.client = openai.OpenAI(base_url=base_url, api_key=api_key)

    def chat(self, model: str, messages: List[Dict[str, str]]) -> str:
        """
        与模型进行对话。

        :param model: 使用的模型名称
        :param messages: 消息列表，包含角色和内容
        :return: 模型回复的内容
        """
        completion = self.client.chat.completions.create(
            model=model,
            messages=messages
        )
        return completion.choices[0].message.content

    def vectorize_text(self, model: str, text: str) -> List[float]:
        """
        将文本向量化。

        :param model: 使用的模型名称
        :param text: 要向量化的文本
        :return: 文本的向量表示
        """
        response = self.client.embeddings.create(
            model=model,
            input=text
        )
        return response.data[0].embedding