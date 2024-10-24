from tinydb import TinyDB

class DB:
    _instance = None

    def __new__(cls, db_file_path: str = r"C:\GZAssistantAppData\data\tinydb.json"):
        if cls._instance is None:
            cls._instance = super(DB, cls).__new__(cls)
            cls._instance.db = TinyDB(db_file_path)
        return cls._instance