import os
import sys
import httpx
from tqdm import tqdm
import subprocess
from typing import Dict, List, Optional
import psutil
import aiofiles
import requests

class Models:
    slm: str = "minicpm3-4b.Q4_0.gguf"
    slm_download_url: str = "https://huggingface.co/mav23/MiniCPM3-4B-GGUF/resolve/main/minicpm3-4b.Q4_0.gguf?download=true"
    embed: str = "bge-large-zh-v1.5-q4_0.gguf"
    # "https://huggingface.co/SmartCreationAI/bge-large-zh-v1.5/resolve/main/bge-large-zh-v1.5-q4_0.gguf?download=true"
    embed_download_url: str = "https://huggingface.co/SmartCreationAI/bge-large-zh-v1.5/resolve/main/bge-large-zh-v1.5-q4_0.gguf?download=true"

def download_file(url: str, output_file: str) -> None:
    response = requests.get(url, stream=True)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open(output_file, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()

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
        embedding: bool = False
) -> None:
    """
    执行 llama-server 命令并记录日志。

    :param model_path: 模型文件的路径
    :param context_length: 上下文长度
    :param port: 监听端口
    :param ngl: 可选的 NGL 参数，默认为 None
    :param run_in_background: 是否在后台运行，默认为 True
    :param embedding: 是否启用 embedding, 默认为 False
    """
    command = [
        'llama-server',
        '-m', model_path,
        '--port', str(port)
    ]

    if embedding:
        command.append('--embedding')
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
    

def run_llama_server(config_file_path: str = r"C:\Users\966\Projects\GuangZhiAssistant-main\server_config.json", run_in_background: bool = True, port: int = 8866):
    # python -m llama_cpp.server --port 8866 --config_file ./server_config.json
    port_str = str(port)
    command = [
        'python',
        '-m', 
        'llama_cpp.server',
        '--port', port_str,
        '--config_file', config_file_path
    ]

    if run_in_background:
        # 在后台运行
        subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        # 在前台运行
        subprocess.run(command, check=True)


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

def stop_llama_server(port: int = 8866):
    # 查找占用指定端口的进程 ID
    find_port_command = f'netstat -ano | findstr :{port}'
    result = subprocess.run(find_port_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    lines = result.stdout.splitlines()
    if not lines:
        print(f'没有找到占用端口 {port} 的进程，无法关闭服务。')
        return
    for line in lines:
        parts = line.split()
        if len(parts) >= 5 and parts[1] == 'TCP':
            pid = parts[4]
            break
    else:
        print(f'没有找到占用端口 {port} 的进程，无法关闭服务。')
        return

    # 根据进程 ID 结束进程
    taskkill_command = f'taskkill /F /PID {pid}'
    subprocess.run(taskkill_command, shell=True, check=True)
    print(f'成功关闭占用端口 {port} 的服务。')


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

    run_llama_server(Models.embed, port=6688, embedding=True, run_in_background=False)