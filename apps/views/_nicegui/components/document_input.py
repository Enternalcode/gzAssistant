from nicegui.ui import input
from nicegui.events import Handler, ValueChangeEventArguments, UiEventArguments, GenericEventArguments
# <class 'nicegui.elements.input.Input'>
from apps.services.db import DB
from tinydb import Query


def document_input() -> input:
    db = DB().db
    options = ['https://', 'http://']
    config_table = db.table('config', cache_size=30)
    query = Query()
    store_value = config_table.search(query.key == "document_url")
    input_value = None
    if len(store_value) == 0:
        default_value = {"value": "https://img-bss.csdnimg.cn/armdasai/Armaipc.html"}
        input_value = default_value
    else:
        input_value = {"value": store_value[0]["value"]}
    
    input_component = input(label='文档网址', placeholder='https://', autocomplete=options).bind_value(input_value, 'value')

     # 定义 on_change 函数
    def on_change(e: GenericEventArguments):
        new_value = e.args
        config_table.update({'value': new_value}, query.key == "document_url")
        if len(config_table.search(query.key == "document_url")) == 0:
            config_table.insert({'key': "document_url", 'value': new_value})

    input_component.on('update:modelValue', on_change)

    return input_component
