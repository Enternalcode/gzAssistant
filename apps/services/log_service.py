import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from nicegui.ui import log
from apps.utils.common import singleton

@singleton
class NiceGuiLogHandler(logging.Handler):
    def __init__(self, log_view: log):
        super().__init__()
        self.log_view = log_view

    def emit(self, record):
        log_entry = self.format(record)
        self.log_view.push(log_entry)

    def format(self, record):
        return f"{record.asctime} - {record.levelname} - {record.getMessage()}"

class LogService:
    def __init__(self, log_directory: str = None, log_view: log = None, name: str = None):
        if log_directory is None:
            self.log_directory = os.path.join("C:", "\\GZAssistantAppData\\logs\\")
        else:
            self.log_directory = log_directory
        os.makedirs(self.log_directory, exist_ok=True)
        self.log_view = log_view
        self.name = name
    
    def add_log_view(self, log_view: log) -> None:
        self.log_view = log_view
        self.setup_logging()

    def setup_logging(self):
        # 使用当前日期生成日志文件名
        current_date = datetime.now().strftime('%Y-%m-%d')
        log_file_path = os.path.join(self.log_directory, f'guangzhi_{current_date}.log')
        
        # 创建一个按天分割的日志处理器，并指定编码为 utf-8
        file_handler = TimedRotatingFileHandler(
            log_file_path, when="midnight", interval=1, backupCount=7, encoding='utf-8'
        )
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
        
        logger = logging.getLogger(name=self.name)
        logger.setLevel(logging.INFO)
        logger.addHandler(file_handler)

        if self.log_view:
            gui_handler = NiceGuiLogHandler(log_view=self.log_view)
            gui_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
            logger.addHandler(gui_handler)

    def info(self, message: str):
        logging.info(message)

    def error(self, message: str):
        logging.error(message)
