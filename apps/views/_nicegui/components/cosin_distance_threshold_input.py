from nicegui.ui import input
from nicegui.events import GenericEventArguments
from apps.services.db import DB
from tinydb import Query
from apps.views._nicegui.components.utils import get_stored_content


default_config_key = "cosin_distance_threshold_input"


def cosin_distance_threshold_input() -> input:
    db = DB().db
    options = ['0.47', '0.42']
    config_table = db.table('config', cache_size=30)
    query = Query()
    sotred_value = get_stored_content(default_config_key)
    input_value = None
    if sotred_value:
        input_value = {"value": sotred_value}
    else:
        default_url = '0.47'
        default_value = {"value": default_url}
        config_table.insert({'key': default_config_key, 'value': default_url})
        input_value = default_value
        
    component = input(label='分数', placeholder='0.47', autocomplete=options).bind_value(input_value, 'value')

    # 定义 on_change 函数
    def on_change(e: GenericEventArguments):
        new_value = e.args
        config_table.update({'value': new_value}, query.key == default_config_key)
        if len(config_table.search(query.key == default_config_key)) == 0:
            config_table.insert({'key': default_config_key, 'value': new_value})

    component.on('update:modelValue', on_change)

    return component
