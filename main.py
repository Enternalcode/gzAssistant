from nicegui import ui
from apps.views._nicegui.main_page import *
from apps.utils.config import create_folders_from_list

def init():
    """
    环境配置
    """
    create_folders_from_list()



init()
ui.run(title="AI广智", dark=False)