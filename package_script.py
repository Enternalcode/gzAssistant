import os
from pathlib import Path
import subprocess
import nicegui

# https://llama-cpp-python.readthedocs.io/en/latest/server/
# C:\Users\966\.pyenv-win-venv\envs\gzAssistant\Lib\site-packages
# C:\Users\966\Projects\GuangZhiAssistant-main\hooks

# pip install llama-cpp-python[server]
    # '--add-data', f'{os.path.abspath("C:\\Users\\966\\Projects\\GuangZhiAssistant-main\\models\\Lite-Mistral-150M-v2-Instruct-Q4_K_S.gguf")}{os.pathsep}models',
cmd = [
    'pyinstaller',
    '--noconfirm',
    '--onedir',
    # '--windowed',
    '--additional-hooks-dir', './hooks',
    '--add-data', f'{Path(nicegui.__file__).parent}{os.pathsep}nicegui',
    '--name', '微信运营AI助手',
    r'C:\Users\966\Projects\GuangZhiAssistant-main\main.py'
]
subprocess.call(cmd)

# """
# pyinstaller --noconfirm --onedir --console --icon "C:\Users\966\Pictures\pbb4c-mlsc0-001.ico" --name "gzaiv1" --add-data "C:\Users\966\.pyenv-win-venv\envs\gzAssistant\Lib\site-packages\nicegui;nicegui/" --additional-hooks-dir "C:\Users\966\Projects\GuangZhiAssistant-main\hooks" --hidden-import "aiofiles" --hidden-import "beautifulsoup4" --hidden-import "fastapi" --hidden-import "hnswlib" --hidden-import "html2text" --hidden-import "httpx" --hidden-import "ifaddr" --hidden-import "libsass" --hidden-import "matplotlib" --hidden-import "nicegui_highcharts" --hidden-import "pyecharts" --hidden-import "Pygments" --hidden-import "python-socketio" --hidden-import "pytest" --hidden-import "selenium" --hidden-import "starlette" --hidden-import "tinydb" --hidden-import "tqdm" --hidden-import "typing_extensions" --hidden-import "uiautomation" --hidden-import "uvicorn" --hidden-import "vbuild" --hidden-import "webview" --add-data "C:\Users\966\Projects\GuangZhiAssistant-main\server_config.json;."  "C:\Users\966\Projects\GuangZhiAssistant-main\main.py"
# """