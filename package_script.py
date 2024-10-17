import os
from pathlib import Path
import subprocess
import nicegui

# https://llama-cpp-python.readthedocs.io/en/latest/server/
# pip install llama-cpp-python[server]
cmd = [
    'pyinstaller',
    '--noconfirm',
    '--onedir',
    '--console',
    '--hidden-import', 'nicegui',
    '--hidden-import', 'asyncio',
    '--additional-hooks-dir', 'C:\\Users\\966\\Projects\\GuangZhiAssistant-main\\hooks',
    '--add-data', f'{Path("nicegui").parent}{os.pathsep}nicegui',
    '--add-data', f'{os.path.abspath("C:\\Users\\966\\Projects\\GuangZhiAssistant-main\\models\\Lite-Mistral-150M-v2-Instruct-Q4_K_S.gguf")}{os.pathsep}models',
    'C:\\Users\\966\\Projects\\GuangZhiAssistant-main\\apps\\views\\_nicegui\\components\\process_document.py'
]
subprocess.call(cmd)

# pyinstaller --noconfirm --onedir --console --hidden-import "nicegui" --hidden-import "asyncio" --additional-hooks-dir "C:\Users\966\Projects\GuangZhiAssistant-main\hooks"  "C:\Users\966\Projects\GuangZhiAssistant-main\apps\views\_nicegui\components\process_document.py"

# pyinstaller --noconfirm --onedir --console --add-data "C:\Users\966\.pyenv-win-venv\envs\gzAssistant\Lib\site-packages\nicegui;nicegui/" --additional-hooks-dir "C:\Users\966\Projects\GuangZhiAssistant-main\hooks" --add-data "C:\Users\966\Projects\GuangZhiAssistant-main\models;models/"  "C:\Users\966\Projects\GuangZhiAssistant-main\apps\views\_nicegui\components\process_document.py"