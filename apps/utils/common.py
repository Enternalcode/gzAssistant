import requests
from tqdm import tqdm
import subprocess
from typing import Dict, Optional
from services import log_service

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

def run_llama_server(model_path: str, context_length: int, port: int, ngl: Optional[int] = None, 
                     run_in_background: bool = True) -> None:
    """
    执行 llama-server 命令并记录日志。

    :param model_path: 模型文件的路径
    :param context_length: 上下文长度
    :param port: 监听端口
    :param ngl: 可选的 NGL 参数，默认为 None
    :param run_in_background: 是否在后台运行，默认为 True
    """
    command = [
        'llama-server',
        '-m', model_path,
        '-c', str(context_length),
        '--port', str(port)
    ]

    if ngl is not None:
        command += ['-ngl', str(ngl)]

    try:
        if run_in_background:
            # 在后台运行
            subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            log_service.log_info("llama-server 已在后台运行。")
        else:
            # 在前台运行
            subprocess.run(command, check=True)
            log_service.log_info("llama-server 在前台运行。")
    except subprocess.CalledProcessError as e:
        log_service.log_error(f"命令执行失败: {e}")
    except Exception as e:
        log_service.log_error(f"发生错误: {e}")

def check_health(url: str) -> Dict[str, str]:
    """
    检查服务的健康状态。

    :param url: 健康检查的 URL
    :return: 包含健康状态信息的字典
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # 如果响应状态码不是 200，将引发异常

        if response.status_code == 200:
            return {"status": "ok"}
        
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 503:
            return {
                "error": {
                    "code": 503,
                    "message": "Loading model",
                    "type": "unavailable_error"
                }
            }
        else:
            return {"error": {"code": response.status_code, "message": str(http_err)}}
    except requests.exceptions.RequestException as req_err:
        return {"error": {"code": 500, "message": str(req_err)}}

    return {"error": {"code": 500, "message": "Unknown error"}}



if __name__ == '__main__':
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
    pass