
import json
import os
import re
import socket
import httpx
from tqdm import tqdm
import subprocess
from typing import Dict, List, Optional
import psutil
import aiofiles

# def download_file(url: str, output_file: str) -> None:
#     response = requests.get(url, stream=True)
#     total_size_in_bytes = int(response.headers.get('content-length', 0))
#     block_size = 1024
#     progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
#     with open(output_file, 'wb') as file:
#         for data in response.iter_content(block_size):
#             progress_bar.update(len(data))
#             file.write(data)
#     progress_bar.close()

def singleton(cls):
    instances = {}
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

async def download_file_async(url: str, output_file: str) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.get(url, stream=True)
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        async with aiofiles.open(output_file, 'wb') as file:
            async for data in response.aiter_content(block_size):
                progress_bar.update(len(data))
                await file.write(data)
        progress_bar.close()

def download_file_sync(url: str, output_file: str) -> None:
    with httpx.stream("GET", url) as r:
        total_size_in_bytes = int(r.headers.get('content-length', 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        with open(output_file, 'wb') as file:
            for data in r.iter_bytes(chunk_size=block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()

def run_llama_server_with_command(
        model_path: str,
        port: int,
        context_length: Optional[int] = None,
        ngl: Optional[int] = None,
        run_in_background: bool = True,
        embedding: bool = False,
        reranking: bool = False
) -> None:
    """
    执行 llama-server 命令并记录日志。

    :param model_path: 模型文件的路径
    :param context_length: 上下文长度
    :param port: 监听端口
    :param ngl: 可选的 NGL 参数，默认为 None
    :param run_in_background: 是否在后台运行，默认为 True
    :param embedding: 是否启用 embedding, 默认为 False
    :param reranking: 是否启用 reranking
    """
    command = [
        'llama-server',
        '-m', model_path,
        '--port', str(port)
    ]

    if embedding:
        command.append('--embedding')
    elif reranking:
        command.append('--reranking')
    else:
        command.append('-c')
        command.append(str(context_length))

    if ngl is not None:
        command += ['-ngl', str(ngl)]

    if run_in_background:
        # 在后台运行
        subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        # 在前台运行
        subprocess.run(command, check=True)

async def check_server_status():
    async with httpx.AsyncClient(proxies={}) as client:
        response = await client.get("http://127.0.0.1:7864/docs")
        if response.status_code == 200:
            return True
        else:
            return False


async def run_llama_server_async(config_file_path: str = r"./server_config.json", run_in_background: bool = True, port: int = 7864):
    # 检查配置文件是否存在
    if not os.path.exists(config_file_path):
        raise FileNotFoundError(f"配置文件 {config_file_path} 不存在。")

    # 检查端口是否在有效范围内
    if not 0 < port < 65536:
        raise ValueError("端口号必须在1到65535之间。")

    # 检查端口是否被占用
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("", port))
        sock.close()
    except socket.error as e:
        raise RuntimeError(f"端口 {port} 已被占用。") from e

    port_str = str(port)
    config_file_abs_path = os.path.abspath(config_file_path)
    command = [
        'python',
        '-m', 
        'llama_cpp.server',
        '--port', port_str,
        '--config_file', config_file_abs_path
    ]

    # 记录日志
    print(f"正在启动AI服务器，命令： {' '.join(command)}")
    if run_in_background:
        # 在后台运行，捕获输出和错误
        subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
    else:
        subprocess.run(command, check=True)


def send_rerank_request(query: str, documents: List[str]):
    # llama-server -m "C:\GZAssistantAppData\models\bge-reranker-v2-m3-Q4_K_M.gguf" --port 8867 --reranking
    url = "http://127.0.0.1:8867/v1/rerank"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "some-model",
        "query": query,
        "top_n": 3,
        "documents": documents
    }
    with httpx.Client() as client:
        response = client.post(url, headers=headers, data=json.dumps(data))
        return response.json()


async def check_health(url: str) -> Dict[str, str]:
    """
    异步检查服务的健康状态。

    :param url: 健康检查的 URL
    :return: 包含健康状态信息的字典
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # 如果响应状态码不是 200，将引发异常

            if response.status_code == 200:
                return {"status": "ok"}
            else:
                return {"error": {"code": response.status_code, "message": response.text}}
    except httpx.HTTPStatusError as http_err:
        if http_err.response.status_code == 503:
            return {
                "error": {
                    "code": 503,
                    "message": "Loading model",
                    "type": "unavailable_error"
                }
            }
        else:
            return {"error": {"code": http_err.response.status_code, "message": http_err.response.text}}
    except httpx.RequestError as req_err:
        return {"error": {"code": 500, "message": str(req_err)}}

def kill_llama_servers():
    """Terminate all processes named 'llama-server.exe'."""
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'llama-server.exe':
            proc.kill()

def stop_llama_server(port: int = 7864):
    kill_process_using_port(port)


def kill_process_using_port(port):
    try:
        result = subprocess.check_output(f'netstat -ano | findstr "{port}"', shell=True).decode()
        lines = result.splitlines()
        for line in lines:
            parts = re.split(r"\s+", line)
            if len(parts) >= 5:
                pid = parts[4]
                try:
                    os.system(f"taskkill /F /PID {pid}")
                    print(f"已杀掉占用端口{port}的进程，PID: {pid}")
                except Exception as e:
                    print(f"杀掉进程{pid}时出错: {e}")
    except Exception as e:
        print(f"查找占用端口{port}的进程时出错: {e}")


if __name__ == '__main__':
    pass
    # Download slm model
    # url = "https://huggingface.co/OuteAI/Lite-Mistral-150M-v2-Instruct-GGUF/resolve/main/Lite-Mistral-150M-v2-Instruct-Q4_K_M.gguf?download=true"
    # output_file = "Lite-Mistral-150M-v2-Instruct-Q4_K_M.gguf"   
    # download_file(url, output_file)

    # Download embedding model
    # url = "https://huggingface.co/SmartCreationAI/bge-large-zh-v1.5/resolve/main/bge-large-zh-v1.5-q4_k_m.gguf?download=true"
    # output_file = "models/bge-large-zh-v1.5-q4_k_m.gguf"
    # download_file(url, output_file)
    

    # Run SLM service
    # run_llama_server('models/Lite-Mistral-150M-v2-Instruct-Q4_K_S.gguf', 2048, 6666, 99)
    # run_llama_server('models/Llama-3.2-3B-Instruct-Q4_0_4_4.gguf', 2048, 6666, 99)
    
    
    # Check health
    # health_url = "http://localhost:6666/health"
    # health_status = check_health(health_url)
    # print(health_status)