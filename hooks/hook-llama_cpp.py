from PyInstaller.utils.hooks import collect_data_files, get_package_paths, collect_submodules
import os, sys


# 处理llama_cpp包
package_path = get_package_paths('llama_cpp')[0]
datas = collect_data_files('llama_cpp')

# 根据操作系统处理动态链接库
if os.name == 'nt':  # Windows
    dll_path = os.path.join(package_path, 'llama_cpp', 'lib', 'llama.dll')
    datas.append((dll_path, 'llama_cpp'))
elif sys.platform == 'darwin':  # Mac
    so_path = os.path.join(package_path, 'llama_cpp', 'libllama.dylib')
    datas.append((so_path, 'llama_cpp'))
elif os.name == 'posix':  # Linux
    so_path = os.join(package_path, 'llama_cpp', 'libllama.so')
    datas.append((so_path, 'llama_cpp'))
