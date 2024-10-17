import httpx
from typing import List, Dict, Any
from apps.utils.common import singleton
TIMEOUT_SECS = 120

proxy_mounts = {
    "http://": httpx.HTTPTransport(proxy="http://localhost:8866"),
    "https://": httpx.HTTPTransport(proxy="http://localhost:8866"),
}

@singleton
class SlmService:
    def __init__(self, base_url: str, api_key: str, logger) -> None:
        self.base_url = base_url
        self.api_key = api_key
        self.logger = logger
    
    def chat_sync(self, messages: List[Dict[str, str]], model: str = "slm", only_msg: bool = True) -> Dict[str, Any] | str:
        url = f"{self.base_url}/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "model": model,
            "messages": messages
        }
        with httpx.Client(mounts=proxy_mounts) as client:
            response = client.post(url, headers=headers, json=payload, timeout=TIMEOUT_SECS)
            if response.status_code != 200:
                self.logger.error(f"Request failed: {response}")
                return response
            json_res = response.json()
            if only_msg:
                return json_res['choices'][0]['message']['content']
            else:
                return json_res

    async def chat_async(self, messages: List[Dict[str, str]], model: str = "slm", only_msg: bool = True) -> Dict[str, Any] | str:
        url = f"{self.base_url}/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "model": model,
            "messages": messages
        }
        
        async with httpx.AsyncClient(mounts=proxy_mounts) as client:
            response = await client.post(url, headers=headers, json=payload, timeout=TIMEOUT_SECS)
            print(response)
            if response.status_code != 200:
                self.logger.error(f"Request failed: {response}")
                return response
            json_res = response.json()
            if only_msg:
                return json_res['choices'][0]['message']['content']
            else:
                return json_res

    def embeddings_sync(self, input_data: str, model: str = "ebed", encoding_format: str = 'float', only_embeds: bool = True) -> Dict[str, Any] | List:
        url = f"{self.base_url}/v1/embeddings"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "input": "hello world",
            "model": model,
            "encoding_format": encoding_format
        }
        
        with httpx.Client(mounts=proxy_mounts) as client:
            response = client.post(url, headers=headers, json=payload, timeout=TIMEOUT_SECS)
            
            if response.status_code != 200:
                self.logger.error(f"Request failed: {response}")
                return response
            
            json_res = response.json()
            if only_embeds:
                return json_res['data'][0]['embedding']
            else:
                return json_res

    async def embeddings_async(self, input_data: str, model: str = "ebed", encoding_format: str = 'float', only_embeds: bool = True) -> Dict[str, Any] | List:
        url = f"{self.base_url}/v1/embeddings"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "input": input_data,
            "model": model,
            "encoding_format": encoding_format
        }
        
        async with httpx.AsyncClient(mounts=proxy_mounts) as client:
            response = await client.post(url, headers=headers, json=payload, timeout=TIMEOUT_SECS)
            
            if response.status_code != 200:
                self.logger.error(f"Request failed: {response}")
                return response
            json_res = response.json()
            if only_embeds:
                return json_res['data'][0]['embedding']
            else:
                return json_res