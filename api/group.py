import aiohttp
import json

class GroupAPI:
    def __init__(self, host: str, port: int):
        self.url = f"http://{host}:{port}"

    async def mute_group_member(self, group_id: str, user_id: str, duration: int):
        """
        禁言群成员。duration 为秒数，0 表示解除禁言。
        参考: /set_group_ban
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
                    raise Exception(f"禁言失败: {result.get('message', '未知错误')}")
                return result

    async def send_group_notice(self, group_id: str, content: str):
        """
        设置群公告。
        参考: /_send_group_notice
        """
        payload = {
            "group_id": group_id,
            "content": content,
            "is_top": True,
            "send_to_new_member": True
        }
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/_send_group_notice", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"设置公告失败: {result.get('message', '未知错误')}")
                return result

    async def set_essence_message(self, group_id: str, message_id: str):
        """
        设置群精华消息。
        参考: /set_essence_msg
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
                    raise Exception(f"设置精华消息失败: {result.get('message', '未知错误')}")
                return result

    async def get_group_info(self, group_id: str):
        """
        获取群信息。
        参考: /get_group_info
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.url}/get_group_info?group_id={group_id}") as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"获取群信息失败: {result.get('message', '未知错误')}")
                return result

    async def get_group_member_list(self, group_id: str):
        """
        获取群成员列表。
        参考: /get_group_member_list
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.url}/get_group_member_list?group_id={group_id}") as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"获取成员列表失败: {result.get('message', '未知错误')}")
                return result

    async def kick_group_member(self, group_id: str, user_id: str, reject_add_request: bool = False):
        """
        踢出群成员。
        参考: /set_group_kick
        """
        payload = {
            "group_id": group_id,
            "user_id": user_id,
            "reject_add_request": reject_add_request
        }
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/set_group_kick", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"踢出成员失败: {result.get('message', '未知错误')}")
                return result

    async def set_group_admin(self, group_id: str, user_id: str, enable: bool):
        """
        设置或取消群管理员。
        参考: /set_group_admin
        """
        payload = {
            "group_id": group_id,
            "user_id": user_id,
            "enable": enable
        }
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/set_group_admin", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"设置管理员失败: {result.get('message', '未知错误')}")
                return result

    async def set_group_name(self, group_id: str, group_name: str):
        """
        设置群名称。
        参考: /set_group_name
        """
        payload = {
            "group_id": group_id,
            "group_name": group_name
        }
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/set_group_name", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"设置群名称失败: {result.get('message', '未知错误')}")
                return result

    async def set_group_special_title(self, group_id: str, user_id: str, special_title: str, duration: int = -1):
        """
        设置群成员特殊头衔。
        参考: /set_group_special_title
        """
        payload = {
            "group_id": group_id,
            "user_id": user_id,
            "special_title": special_title,
            "duration": duration  # -1 表示永久
        }
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/set_group_special_title", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"设置特殊头衔失败: {result.get('message', '未知错误')}")
                return result

    async def get_group_at_all_remain(self, group_id: str):
        """
        获取群@全体剩余次数。
        参考: /get_group_at_all_remain
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.url}/get_group_at_all_remain?group_id={group_id}") as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"获取@全体剩余次数失败: {result.get('message', '未知错误')}")
                return result

    async def get_group_mute_list(self, group_id: str):
        """
        获取群禁言列表。
        参考: /get_group_mute_list
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.url}/get_group_mute_list?group_id={group_id}") as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"获取禁言列表失败: {result.get('message', '未知错误')}")
                return result

    async def send_group_poke(self, group_id: str, user_id: str):
        """
        发送群聊戳一戳。
        参考: /group_poke
        """
        payload = {
            "group_id": group_id,
            "user_id": user_id
        }
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/group_poke", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"发送戳一戳失败: {result.get('message', '未知错误')}")
                return result

    async def send_like(self, user_id: str, times: int):
        """
        为用户点赞。
        参考: /send_like
        """
        payload = {
            "user_id": user_id,
            "times": times
        }
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/send_like", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"点赞失败: {result.get('message', '未知错误')}")
                return result

    async def handle_group_request(self, flag: str, approve: bool):
        """
        处理加群请求。
        参考: /set_group_add_request
        """
        payload = {
            "flag": flag,
            "approve": approve
        }
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/set_group_add_request", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"处理加群请求失败: {result.get('message', '未知错误')}")
                return result

    async def move_group_file(self, group_id: str, file_id: str, target_dir: str):
        """
        移动群文件。
        参考: /move_group_file
        """
        payload = {
            "group_id": group_id,
            "file_id": file_id,
            "target_dir": target_dir
        }
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/move_group_file", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"移动群文件失败: {result.get('message', '未知错误')}")
                return result

    async def upload_group_file(self, group_id: str, file_url: str):
        """
        上传群文件。
        参考: /upload_group_file
        """
        payload = {
            "group_id": group_id,
            "url": file_url
        }
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/upload_group_file", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"上传群文件失败: {result.get('message', '未知错误')}")
                return result

    async def set_typing_status(self, group_id: str):
        """
        设置输入状态。
        参考: /set_typing_status
        """
        payload = {
            "group_id": group_id
        }
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/set_typing_status", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"设置输入状态失败: {result.get('message', '未知错误')}")
                return result