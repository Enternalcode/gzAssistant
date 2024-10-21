from tinydb import Query
from apps.services.db import DB
from contextlib import contextmanager
from nicegui import ui

def get_stored_content(config_key: str):
    db = DB().db
    config_table = db.table('config', cache_size=30)
    query = Query()
    store_value = config_table.search(query.key == config_key)
    if store_value:
        return store_value[0]["value"]
    return None


@contextmanager
def disable(button: ui.button):
    button.disable()
    try:
        yield
    finally:
        button.enable()