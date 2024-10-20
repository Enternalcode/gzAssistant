python main.py

pyenv-win-venv activate gzAssistant

pyenv-win-venv activate gzAssistant & python main.py

# Kill llama-server
netstat -ano | findstr "7864"
tasklist | findstr "llama-server.exe"
taskkill /F /PID <process_id>


# 需求
场景 + 诱因 + 目的 + 结果