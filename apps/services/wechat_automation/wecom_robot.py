from typing import Any, Literal
import requests
import json


class WeComRobot:
    def __init__(self, webhook_url: str = None) -> None:
        if webhook_url is None:
            # webhook_url = sensitive_config['WECOM_ROBOT_WEBHOOK']
            pass
        self.webhook_url = webhook_url
    
    def _send_text(self, content: Any) -> Any:
        data = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.webhook_url, headers=headers, data=json.dumps(data))
        return response.json()

    def send_message(self, content: Any, msg_type: Literal['text']) -> Any:
        if msg_type == 'text':
            self._send_text(content=content)
        else:
            raise ValueError('Current unsupported msg types')
