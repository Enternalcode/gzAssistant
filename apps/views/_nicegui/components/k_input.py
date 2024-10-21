from nicegui.ui import input
from nicegui.events import GenericEventArguments
from apps.services.db import DB
from tinydb import Query
from apps.views._nicegui.components.utils import get_stored_content


default_config_key = "k"


def k_input() -> input:
    db = DB().db
    options = ['3', '5']
    config_table = db.table('config', cache_size=30)
    query = Query()
    stored_content = get_stored_content(default_config_key)
    input_value = None
    if stored_content:
        input_value = {"value": stored_content}
    else:
        default_url = "3"
        default_value = {"value": default_url}
        config_table.insert({'key': default_config_key, 'value': default_url})
        input_value = default_value
        
    input_component = input(label='检索返回条数', placeholder='3', autocomplete=options).bind_value(input_value, 'value').tooltip("每次检索知识库返回的数据条数，注意：知识库内总数据条数必须大于此值")

    # 定义 on_change 函数
    def on_change(e: GenericEventArguments):
        new_value = e.args
        config_table.update({'value': new_value}, query.key == default_config_key)
        if len(config_table.search(query.key == default_config_key)) == 0:
            config_table.insert({'key': default_config_key, 'value': new_value})

    input_component.on('update:modelValue', on_change)

    return input_component
