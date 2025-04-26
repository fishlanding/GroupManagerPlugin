import aiohttp
import json
from pkg.platform.types import MessageChain

class MessageAPI:
    def __init__(self, host: str, port: int):
        self.url = f"http://{host}:{port}"

    async def send_group_message(self, group_id: str, message_chain: MessageChain):
        """
        Send a message to a group.
        Ref: 
        """
        payload = {
            "group_id": group_id,
            "message": message_chain
        }
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/send_group_msg", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"Failed to send message: {result.get('message', 'Unknown error')}")
                return result