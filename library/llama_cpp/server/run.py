from __future__ import annotations

import os
import uvicorn
from library.llama_cpp.server.settings import (
    ServerSettings,
    ConfigFileSettings,
)
from library.llama_cpp.server.__main__ import create_app

def start_server(config_file: str, host: str, port: int):
    with open(config_file, "rb") as f:
        # 检查是否为yaml文件
        if config_file.endswith(".yaml") or config_file.endswith(".yml"):
            import yaml
            import json
            config_file_settings = ConfigFileSettings.model_validate_json(
                json.dumps(yaml.safe_load(f))
            )
        else:
            config_file_settings = ConfigFileSettings.model_validate_json(f.read())
        server_settings = ServerSettings.model_validate(config_file_settings)
        model_settings = config_file_settings.models
    app = create_app(
        server_settings=server_settings,
        model_settings=model_settings,
    )
    uvicorn.run(
        app,
        host=host,
        port=port,
        ssl_keyfile=server_settings.ssl_keyfile,
        ssl_certfile=server_settings.ssl_certfile,
    )
