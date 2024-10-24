from nicegui.ui import input
from nicegui.events import GenericEventArguments
from apps.services.db import DB
from tinydb import Query
from apps.views._nicegui.components.utils import get_stored_content


default_config_key = "document_url"


def document_input() -> input:
    db = DB().db
    options = ['https://', 'http://']
    config_table = db.table('config', cache_size=30)
    query = Query()
    stored_document_url = get_stored_content(default_config_key)
    input_value = None
    if stored_document_url:
        input_value = {"value": stored_document_url}
    else:
        default_url = "https://img-bss.csdnimg.cn/armdasai/Armaipc.html"
        default_value = {"value": default_url}
        config_table.insert({'key': default_config_key, 'value': default_url})
        input_value = default_value
        
    input_component = input(label='文档网址', placeholder='https://', autocomplete=options).bind_value(input_value, 'value')

    # 定义 on_change 函数
    def on_change(e: GenericEventArguments):
        new_value = e.args
        config_table.update({'value': new_value}, query.key == default_config_key)
        if len(config_table.search(query.key == default_config_key)) == 0:
            config_table.insert({'key': default_config_key, 'value': new_value})

    input_component.on('update:modelValue', on_change)

    return input_component
