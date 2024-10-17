from nicegui import ui
from time import sleep

# 创建一个日志视图组件，用于显示日志
run_log = ui.log(max_lines=50).classes('w-full h-50')

def update_log_view(log_file_path):
    """
    从日志文件中读取最新内容，并将其推送到日志视图组件中。
    
    :param log_file_path: 日志文件的路径
    """
    with open(log_file_path, 'r') as file:
        # 读取文件到一个字符串中
        log_content = file.read()
        # 将日志内容推送到日志视图组件
        run_log.push(log_content)

# 假设你的日志文件路径是 'path/to/your/logfile.log'
log_file_path = 'path/to/your/logfile.log'

# 定期更新日志视图
while True:
    update_log_view(log_file_path)
    # 等待一段时间，例如1秒，然后再次更新
    sleep(1)