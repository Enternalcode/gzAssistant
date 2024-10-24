from nicegui.ui import input
from nicegui.events import GenericEventArguments
from apps.services.db import DB
from tinydb import Query
from apps.views._nicegui.components.utils import get_stored_content


default_config_key = "detection_frequency"

def detection_frequency_input() -> input:
    db = DB().db
    options = ['3', '5', '15']
    config_table = db.table('config', cache_size=30)
    query = Query()
    stored_content = get_stored_content(default_config_key)
    input_value = None
    if stored_content:
        input_value = {"value": stored_content}
    else:
        default_url = "5"
        default_value = {"value": default_url}
        config_table.insert({'key': default_config_key, 'value': default_url})
        input_value = default_value
        
    input_component = input(label='监听频率', placeholder='5', autocomplete=options).bind_value(input_value, 'value').tooltip("每几秒扫描一次群内最消息")

    # 定义 on_change 函数
    def on_change(e: GenericEventArguments):
        new_value = e.args
        config_table.update({'value': new_value}, query.key == default_config_key)
        if len(config_table.search(query.key == default_config_key)) == 0:
            config_table.insert({'key': default_config_key, 'value': new_value})

    input_component.on('update:modelValue', on_change)

    return input_component
