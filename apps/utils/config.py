import json
from typing import Dict

def read_json_config(file_path) -> Dict:
    """
    读取指定路径的 JSON 配置文件，并返回 Python 字典对象。

    :param file_path: JSON 文件的路径
    :return: 包含配置数据的 Python 字典
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"错误：文件 '{file_path}' 未找到。")
        return None
    except json.JSONDecodeError:
        print(f"错误：文件 '{file_path}' 不是有效的 JSON 格式。")
        return None
    except Exception as e:
        print(f"读取文件 '{file_path}' 时发生错误：{e}")
        return None


default_config_path = "apps\config.json"
default_config = read_json_config(default_config_path)