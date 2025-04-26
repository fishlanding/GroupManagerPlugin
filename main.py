from pkg.platform.types import MessageChain
from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  
from pkg.platform.types import *
import re
from plugins.GroupManagerPlugin.api.group import GroupAPI
from plugins.GroupManagerPlugin.api.message import MessageAPI

@register(name="GroupManagerPlugin", description="QQ群管理插件，支持@全体、禁言、公告、设置群精华等功能", version="0.1", author="YuWan_SAMA")
class GroupManagerPlugin(BasePlugin):
    def __init__(self, host: APIHost):
        super().__init__(host)
        self.ap = host
        self.group_api = GroupAPI(host="127.0.0.1", port=3000)
        self.message_api = MessageAPI(host="127.0.0.1", port=3000)

    async def initialize(self):
        pass

    @handler(GroupMessageReceived)
    async def group_message_received(self, ctx: EventContext):
        msg = str(ctx.event.message_chain).strip()
        group_id = str(ctx.event.launcher_id)
        sender_id = str(ctx.event.sender_id)

        # Check if command starts with '/group'
        if not re.match(r'^/group\s+', msg, re.IGNORECASE):
            return

        command = msg.lower().split()
        if len(command) < 2:
            await self.message_api.send_group_message(group_id, MessageChain(["使用方法: /group [atall|mute|unmute|announce|essence] [参数]"]))
            return

        try:
            if command[1] == "atall":
                await self.message_api.send_group_message(group_id, MessageChain([{
                    "type": "at",
                    "data": {"qq": "all"}
                }, " 全体成员"]))

            elif command[1] == "mute":
                if len(command) < 4:
                    await self.message_api.send_group_message(group_id, MessageChain(["使用方法: /group mute <QQ号> <分钟>"]))
                    return
                target_qq = command[2]
                duration = int(command[3]) * 60  # Convert minutes to seconds
                await self.group_api.mute_group_member(group_id, target_qq, duration)
                await self.message_api.send_group_message(group_id, MessageChain([f"已禁言 {target_qq} {command[3]}分钟"]))

            elif command[1] == "unmute":
                if len(command) < 3:
                    await self.message_api.send_group_message(group_id, MessageChain(["使用方法: /group unmute <QQ号>"]))
                    return
                target_qq = command[2]
                await self.group_api.mute_group_member(group_id, target_qq, 0)
                await self.message_api.send_group_message(group_id, MessageChain([f"已解除 {target_qq} 的禁言"]))

            elif command[1] == "announce":
                if len(command) < 3:
                    await self.message_api.send_group_message(group_id, MessageChain(["使用方法: /group announce <公告内容>"]))
                    return
                content = " ".join(command[2:])
                await self.group_api.set_group_notice(group_id, content)
                await self.message_api.send_group_message(group_id, MessageChain(["公告已发布"]))

            elif command[1] == "essence":
                if len(command) < 3:
                    await self.message_api.send_group_message(group_id, MessageChain(["使用方法: /group essence <消息ID>"]))
                    return
                message_id = command[2]
                await self.group_api.set_essence_message(group_id, message_id)
                await self.message_api.send_group_message(group_id, MessageChain(["已设置群精华消息"]))

            else:
                await self.message_api.send_group_message(group_id, MessageChain(["未知命令。支持: atall, mute, unmute, announce, essence"]))

        except Exception as e:
            await self.message_api.send_group_message(group_id, MessageChain([f"错误: {str(e)}"]))

    def __del__(self):
        pass