import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

class LogService:
    def __init__(self, log_directory: str = '~/gzAssistant/logs/'):
        self.log_directory = os.path.expanduser(log_directory)
        os.makedirs(self.log_directory, exist_ok=True)
        self.setup_logging()

    def setup_logging(self):
        # 使用当前日期生成日志文件名
        current_date = datetime.now().strftime('%Y-%m-%d')
        log_file_path = os.path.join(self.log_directory, f'guangzhi_{current_date}.log')
        
        # 创建一个按天分割的日志处理器
        handler = TimedRotatingFileHandler(
            log_file_path, when="midnight", interval=1, backupCount=7
        )
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

    def log_info(self, message: str):
        logging.info(message)

    def log_error(self, message: str):
        logging.error(message)

# 实例化日志服务
log_service = LogService()