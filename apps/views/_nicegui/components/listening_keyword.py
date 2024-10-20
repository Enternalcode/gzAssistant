from nicegui import ui
from nicegui.events import GenericEventArguments
from apps.services.db import DB
from tinydb import Query
from apps.views._nicegui.components.utils import get_stored_content


default_config_key = "listening_keyword"


def listening_keyword_input() -> input:
    db = DB().db
    options = ['@']
    config_table = db.table('config', cache_size=30)
    query = Query()
    stored_content = get_stored_content(default_config_key)
    input_value = None
    if stored_content:
        input_value = {"value": stored_content}
    else:
        default_content = "@群AI助手"
        default_value = {"value": default_content}
        config_table.insert({'key': default_config_key, 'value': default_content})
        input_value = default_value
    
    input_component = ui.input(label='监听关键词', placeholder='@AI助手', autocomplete=options).bind_value(input_value, 'value').tooltip("群聊任何消息以此关键词开头,都会触发AI,请谨慎选择关键词")

    # 定义 on_change 函数
    def on_change(e: GenericEventArguments):
        new_value = e.args
        config_table.update({'value': new_value}, query.key == default_config_key)
        if len(config_table.search(query.key == default_config_key)) == 0:
            config_table.insert({'key': default_config_key, 'value': new_value})

    input_component.on('update:modelValue', on_change)

    return input_component
