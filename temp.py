from __future__ import annotations

import os
import uvicorn
from library.llama_cpp.server.settings import (
    ServerSettings,
    ConfigFileSettings,
)
from library.llama_cpp.server.__main__ import create_app

def main(config_file: str):
    if not os.path.exists(config_file):
        raise ValueError(f"Config file {config_file} not found!")
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
        host=os.getenv("HOST", server_settings.host),
        port=int(os.getenv("PORT", server_settings.port)),
        ssl_keyfile=server_settings.ssl_keyfile,
        ssl_certfile=server_settings.ssl_certfile,
    )


if __name__ == "__main__":
    main(config_file=r"C:\Users\966\Projects\GuangZhiAssistant-main\configs\server_config.json")