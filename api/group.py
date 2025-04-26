import aiohttp
import json

class GroupAPI:
    def __init__(self, host: str, port: int):
        self.url = f"http://{host}:{port}"

    async def mute_group_member(self, group_id: str, user_id: str, duration: int):
        """
        Mute a group member. Duration in seconds (0 to unmute).
        Ref:
        """
        payload = {
            "group_id": group_id,
            "user_id": user_id,
            "duration": duration
        }
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/set_group_ban", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"Failed to mute member: {result.get('message', 'Unknown error')}")
                return result

    async def set_group_notice(self, group_id: str, content: str):
        """
        Set group announcement.
        Ref: 
        """
        payload = {
            "group_id": group_id,
            "content": content,
            "is_top": True,
            "send_to_new_member": True
        }
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/set_group_notice", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"Failed to set notice: {result.get('message', 'Unknown error')}")
                return result

    async def set_essence_message(self, group_id: str, message_id: str):
        """
        Set a message as group essence.
        Ref: 
        """
        payload = {
            "group_id": group_id,
            "message_id": message_id
        }
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/set_essence_msg", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"Failed to set essence message: {result.get('message', 'Unknown error')}")
                return result