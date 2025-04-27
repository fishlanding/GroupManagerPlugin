import aiohttp
import json
from pkg.platform.types import *

class MessageAPI:
    def __init__(self, host: str, port: int):
        self.url = f"http://{host}:{port}"

    async def send_group_message(self, group_id: str, message_chain: list):
        """Send group message."""
        payload = {"group_id": group_id, "message": message_chain}
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/send_group_msg", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"发送消息失败: {result.get('message', '未知错误')}")
                return result

    async def send_group_image(self, group_id: str, image_url: str):
        """Send group image."""
        message_chain = [{"type": "image", "url": image_url}]
        return await self.send_group_message(group_id, message_chain)

    async def send_group_voice(self, group_id: str, voice_url: str):
        """Send group voice."""
        message_chain = [{"type": "voice", "url": voice_url}]
        return await self.send_group_message(group_id, message_chain)

    async def send_group_json(self, group_id: str, json_content: str):
        """Send group JSON message."""
        message_chain = [{"type": "json", "data": json_content}]
        return await self.send_group_message(group_id, message_chain)

    async def send_group_reply(self, group_id: str, message_id: str, content: str):
        """Send group reply message."""
        message_chain = [{"type": "reply", "id": message_id}, {"type": "text", "text": content}]
        return await self.send_group_message(group_id, message_chain)

    async def recall_group_message(self, group_id: str, message_id: str):
        """Recall group message."""
        payload = {"message_id": message_id}
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/delete_msg", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"撤回消息失败: {result.get('message', '未知错误')}")
                return result

    async def ocr_image(self, image_url: str):
        """Perform OCR on image."""
        payload = {"image_url": image_url}
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/ocr_image", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"OCR识别失败: {result.get('message', '未知错误')}")
                return result.get('text', '无法识别文本')

    async def send_group_text(self, group_id: str, content: str):
        """Send group text message."""
        message_chain = [{"type": "text", "text": content}]
        return await self.send_group_message(group_id, message_chain)