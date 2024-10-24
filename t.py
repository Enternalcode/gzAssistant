import os
import socket
from your_module import main  # Replace with the actual import path of your main function
import threading

def run_llama_server(config_file_path: str, port: int):
    # Set environment variables if needed
    os.environ["PORT"] = str(port)
    
    # Call the main function directly
    main(config_file=config_file_path)

async def run_llama_server_async(
    config_file_path: str = r"configs/server_config.json",
    run_in_background: bool = True,
    port: int = 7864
):
    # 检查配置文件是否存在
    if not os.path.exists(config_file_path):
        raise FileNotFoundError(f"配置文件 {config_file_path} 不存在。")

    # 检查端口是否在有效范围内
    if not 0 < port < 65536:
        raise ValueError("端口号必须在1到65535之间。")

    # 检查端口是否被占用
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(("", port))
            except socket.error as e:
                raise ConnectionError(f"端口 {port} 已被占用。") from e
    except Exception as e:
        print(f"检查端口时出错: {e}")
        raise

    # 记录日志
    print(f"正在启动AI服务器，配置文件路径: {config_file_path}")

    try:
        if run_in_background:
            thread = threading.Thread(target=run_llama_server, args=(config_file_path, port))
            thread.start()
            # 可以在这里添加对线程的管理逻辑
        else:
            run_llama_server(config_file_path, port)
    except Exception as e:
        print(f"启动服务器时出错: {e}")
        raise