import aiohttp
import json

class GroupAPI:
    def __init__(self, host: str, port: int):
        self.url = f"http://{host}:{port}"

    async def mute_group_member(self, group_id: str, user_id: str, duration: int):
        """Mute group member."""
        payload = {"group_id": group_id, "user_id": user_id, "duration": duration}
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/set_group_ban", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"禁言失败: {result.get('message', '未知错误')}")
                return result

    async def send_group_notice(self, group_id: str, content: str):
        """Send group notice."""
        payload = {"group_id": group_id, "content": content, "is_top": True, "send_to_new_member": True}
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/_send_group_notice", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"设置公告失败: {result.get('message', '未知错误')}")
                return result

    async def set_essence_message(self, group_id: str, message_id: str):
        """Set essence message."""
        payload = {"group_id": group_id, "message_id": message_id}
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/set_essence_msg", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"设置精华消息失败: {result.get('message', '未知错误')}")
                return result

    async def get_group_info(self, group_id: str):
        """Get group info."""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.url}/get_group_info?group_id={group_id}") as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"获取群信息失败: {result.get('message', '未知错误')}")
                return result

    async def get_group_member_list(self, group_id: str):
        """Get group member list."""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.url}/get_group_member_list?group_id={group_id}") as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"获取成员列表失败: {result.get('message', '未知错误')}")
                return result

    async def kick_group_member(self, group_id: str, user_id: str, reject_add_request: bool = False):
        """Kick group member."""
        payload = {"group_id": group_id, "user_id": user_id, "reject_add_request": reject_add_request}
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/set_group_kick", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"踢出成员失败: {result.get('message', '未知错误')}")
                return result

    async def set_group_admin(self, group_id: str, user_id: str, enable

: bool):
        """Set or unset group admin."""
        payload = {"group_id": group_id, "user_id": user_id, "enable": enable}
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/set_group_admin", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"设置管理员失败: {result.get('message', '未知错误')}")
                return result

    async def set_group_name(self, group_id: str, group_name: str):
        """Set group name."""
        payload = {"group_id": group_id, "group_name": group_name}
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/set_group_name", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"设置群名称失败: {result.get('message', '未知错误')}")
                return result

    async def set_group_special_title(self, group_id: str, user_id: str, special_title: str, duration: int = -1):
        """Set group member special title."""
        payload = {"group_id": group_id, "user_id": user_id, "special_title": special_title, "duration": duration}
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/set_group_special_title", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"设置特殊头衔失败: {result.get('message', '未知错误')}")
                return result

    async def get_group_at_all_remain(self, group_id: str):
        """Get remaining @all count."""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.url}/get_group_at_all_remain?group_id={group_id}") as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"获取@全体剩余次数失败: {result.get('message', '未知错误')}")
                return result

    async def get_group_mute_list(self, group_id: str):
        """Get group mute list."""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.url}/get_group_mute_list?group_id={group_id}") as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"获取禁言列表失败: {result.get('message', '未知错误')}")
                return result

    async def send_group_poke(self, group_id: str, user_id: str):
        """Send group poke."""
        payload = {"group_id": group_id, "user_id": user_id}
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/group_poke", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"发送戳一戳失败: {result.get('message', '未知错误')}")
                return result

    async def send_like(self, user_id: str, times: int):
        """Send like to user."""
        payload = {"user_id": user_id, "times": times}
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/send_like", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"点赞失败: {result.get('message', '未知错误')}")
                return result

    async def handle_group_request(self, flag: str, approve: bool):
        """Handle group join request."""
        payload = {"flag": flag, "approve": approve}
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/set_group_add_request", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"处理加群请求失败: {result.get('message', '未知错误')}")
                return result

    async def move_group_file(self, group_id: str, file_id: str, target_dir: str):
        """Move group file."""
        payload = {"group_id": group_id, "file_id": file_id, "target_dir": target_dir}
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/move_group_file", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"移动群文件失败: {result.get('message', '未知错误')}")
                return result

    async def upload_group_file(self, group_id: str, file_url: str):
        """Upload group file."""
        payload = {"group_id": group_id, "url": file_url}
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/upload_group_file", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"上传群文件失败: {result.get('message', '未知错误')}")
                return result

    async def set_typing_status(self, group_id: str):
        """Set typing status."""
        payload = {"group_id": group_id}
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/set_typing_status", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"设置输入状态失败: {result.get('message', '未知错误')}")
                return result

    async def set_welcome_message(self, group_id: str, content: str):
        """Set welcome message (placeholder, as NapCat may not support this)."""
        # Note: This is a placeholder. NapCat may not have an API for welcome messages.
        # Store in a local config or extend with custom logic if supported.
        payload = {"group_id": group_id, "welcome_message": content}
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/set_welcome_message", data=json.dumps(payload), headers=headers) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"设置欢迎消息失败: {result.get('message', '未知错误')}")
                return result