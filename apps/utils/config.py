
import os
from typing import Dict, List
from tinydb import Query
from apps.services.db import DB

APPLICATION_DATA_PATH = "C:\\GZAssistantAppData"

basic_app_data_folders = [
        'logs', 
        'config', 
        'models',
        'data',
        'embedding'
]

def create_folders_from_list(input_list: List[str] = basic_app_data_folders) -> None:
    for item in input_list:
        folder_path = os.path.join(APPLICATION_DATA_PATH, item)
        os.makedirs(folder_path, exist_ok=True)

def get_config(key: str) -> Dict:
    db = DB().db
    config_table = db.table('config', cache_size=30)
    query = Query()
    store_value = config_table.search(query.key == key)
    return store_value[0].get('value') if store_value else store_value

def init_set_config() -> None:
    db = DB().db
    config_table = db.table('config', cache_size=30)
    default_configs = [
        {
            "key": "distance_threshold", "value": 0.47
        }
    ]
    query = Query()
    for default_config in default_configs:
        config_table.update({'value': default_config['value']}, query.key == default_config['key'])
        if len(config_table.search(query.key == default_config['key'])) == 0:
            config_table.insert({'key': default_config['key'], 'value': default_config['value']})

