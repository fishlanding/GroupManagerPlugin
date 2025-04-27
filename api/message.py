import aiohttp
import json
from pkg.platform.types import MessageChain, Plain, Image, Voice, Face, Json, Reply

class MessageAPI:
    def __init__(self, host: str, port: int):
        self.url = f"http://{host}:{port}"

    async def send_group_message(self, group_id: str, message_chain: MessageChain):
        """
        发送群消息。
        参考: /send_group_msg
        """
        payload = {
            "group_id": group_id,
            "message": message_chain.to_dict() if hasattr(message_chain, 'to_dict') else str(message_chain)
        }
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/send_group_msg", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"发送消息失败: {result.get('message', '未知错误')}")
                return result

    async def send_group_image(self, group_id: str, image_url: str):
        """
        发送群图片。
        参考: /send_group_msg
        """
        message_chain = MessageChain([Image(url=image_url)])
        return await self.send_group_message(group_id, message_chain)

    async def send_group_voice(self, group_id: str, voice_url: str):
        """
        发送群语音。
        参考: /send_group_msg
        """
        message_chain = MessageChain([Voice(url=voice_url)])
        return await self.send_group_message(group_id, message_chain)

    async def send_group_face(self, group_id: str, face_id: str):
        """
        发送群系统表情。
        参考: /send_group_msg
        """
        message_chain = MessageChain([Face(id=face_id)])
        return await self.send_group_message(group_id, message_chain)

    async def send_group_json(self, group_id: str, json_content: str):
        """
        发送群JSON消息。
        参考: /send_group_msg
        """
        message_chain = MessageChain([Json(data=json_content)])
        return await self.send_group_message(group_id, message_chain)

    async def send_group_reply(self, group_id: str, message_id: str, content: str):
        """
        发送群回复消息。
        参考: /send_group_msg
        """
        message_chain = MessageChain([
            Reply(message_id=message_id),
            Plain(text=content)
        ])
        return await self.send_group_message(group_id, message_chain)

    async def recall_group_message(self, group_id: str, message_id: str):
        """
        撤回群消息。
        参考: /delete_msg
        """
        payload = {
            "message_id": message_id
        }
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/delete_msg", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"撤回消息失败: {result.get('message', '未知错误')}")
                return result

    async def ocr_image(self, image_url: str):
        """
        图片OCR识别。
        参考: /ocr_image
        """
        payload = {
            "image_url": image_url
        }
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/ocr_image", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"OCR识别失败: {result.get('message', '未知错误')}")
                return result.get('text', '无法识别文本')

    async def send_group_text(self, group_id: str, content: str):
        """
        发送群纯文本消息。
        参考: /send_group_msg
        """
        message_chain = MessageChain([Plain(text=content)])
        return await self.send_group_message(group_id, message_chain)