import logging
from pkg.plugin.context import register, handler, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *
from plugins.GroupManagerPlugin.api.group import GroupAPI
from plugins.GroupManagerPlugin.api.message import MessageAPI
from plugins.GroupManagerPlugin.api.utils import *

@register(
    name="GroupManagerPlugin",
    description="基于LangBot-NapCat的QQ群管理插件，支持多种群聊管理功能",
    version="0.5",
    author="YuWan_SAMA"
)
class GroupManagerPlugin(BasePlugin):
    def __init__(self, host: APIHost):
        super().__init__(host)
        self.ap = host
        self.group_api = GroupAPI(host="127.0.0.1", port=3000)
        self.message_api = MessageAPI(host="127.0.0.1", port=3000)
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        self.logger = logging.getLogger(__name__)

    async def initialize(self):
        self.logger.info("GroupManagerPlugin initialized")

    async def _send_error(self, group_id: str, message: str):
        """Send error message to group."""
        await self.message_api.send_group_message(group_id, [message])
        self.logger.error(f"Error in group {group_id}: {message}")

    async def _get_help_text(self) -> str:
        """Return help text for commands."""
        return (
            "群管理插件命令列表:\n"
            "/group atall <消息> - @全体成员\n"
            "/group mute <QQ号> <分钟> - 禁言成员\n"
            "/group unmute <QQ号> - 解除禁言\n"
            "/group announce <内容> - 发布公告\n"
            "/group essence <消息ID> - 设置精华消息\n"
            "/group info - 查看群信息\n"
            "/group members - 查看群成员列表\n"
            "/group kick <QQ号> - 踢出成员\n"
            "/group setadmin <QQ号> <true|false> - 设置/取消管理员\n"
            "/group setname <新群名> - 修改群名\n"
            "/group settitle <QQ号> <头衔> - 设置成员头衔\n"
            "/group atallcount - 查看@全体剩余次数\n"
            "/group mutelist - 查看禁言列表\n"
            "/group poke <QQ号> - 戳一戳\n"
            "/group like <QQ号> <次数> - 点赞\n"
            "/group sendimg <图片URL> - 发送图片\n"
            "/group sendvoice <语音URL> - 发送语音\n"
            "/group sendjson <JSON内容> - 发送JSON消息\n"
            "/group reply <消息ID> <内容> - 回复消息\n"
            "/group recall <消息ID> - 撤回消息\n"
            "/group movefile <文件ID> <目标目录> - 移动群文件\n"
            "/group uploadfile <文件URL> - 上传群文件\n"
            "/group ocr <图片URL> - 图片OCR识别\n"
            "/group typing - 设置输入状态\n"
            "/group sendtext <内容> - 发送纯文本消息\n"
            "/group setwelcome <内容> - 设置入群欢迎消息\n"
            "/group approve|reject <QQ号> <flag> - 处理加群请求"
        )

    @handler(GroupCommandSent)
    async def group_command_sent(self, ctx: EventContext):
        event = ctx.event
        if not event or not event.is_admin:
            cmd = event.text_message.strip().split()[0] if event.text_message else "/"
            await self._send_error(event.launcher_id, f"执行 {cmd} 失败: 需要管理员权限")
            return

        msg = event.text_message.strip().lower().split()
        group_id = str(event.launcher_id)
        if len(msg) < 1 or msg[0] != "/group":
            return

        if len(msg) < 2:
            await self.message_api.send_group_message(group_id, [await self._get_help_text()])
            return

        cmd = msg[1]
        try:
            if cmd == "help":
                await self.message_api.send_group_message(group_id, [await self._get_help_text()])

            elif cmd == "atall":
                if len(msg) < 3:
                    await self._send_error(group_id, "使用方法: /group atall <消息内容>")
                    return
                await self.message_api.send_group_message(group_id, [{"type": "at", "qq": "all"}, " ".join(msg[2:])])

            elif cmd == "mute":
                if len(msg) < 4 or not validate_qq(msg[2]) or not validate_duration(msg[3]):
                    await self._send_error(group_id, "使用方法: /group mute <QQ号> <分钟>")
                    return
                duration = int(msg[3]) * 60
                await self.group_api.mute_group_member(group_id, msg[2], duration)
                await self.message_api.send_group_message(group_id, [f"已禁言 {msg[2]} {msg[3]}分钟"])

            elif cmd == "unmute":
                if len(msg) < 3 or not validate_qq(msg[2]):
                    await self._send_error(group_id, "使用方法: /group unmute <QQ号>")
                    return
                await self.group_api.mute_group_member(group_id, msg[2], 0)
                await self.message_api.send_group_message(group_id, [f"已解除 {msg[2]} 的禁言"])

            elif cmd == "announce":
                if len(msg) < 3:
                    await self._send_error(group_id, "使用方法: /group announce <公告内容>")
                    return
                content = " ".join(msg[2:])
                await self.group_api.send_group_notice(group_id, content)
                await self.message_api.send_group_message(group_id, ["公告已发布"])

            elif cmd == "essence":
                if len(msg) < 3:
                    await self._send_error(group_id, "使用方法: /group essence <消息ID>")
                    return
                await self.group_api.set_essence_message(group_id, msg[2])
                await self.message_api.send_group_message(group_id, ["已设置群精华消息"])

            elif cmd == "info":
                group_info = await self.group_api.get_group_info(group_id)
                info_msg = (
                    f"群ID: {group_info['group_id']}\n"
                    f"群名: {group_info['group_name']}\n"
                    f"成员数: {group_info['member_count']}\n"
                    f"最大成员数: {group_info['max_member_count']}"
                )
                await self.message_api.send_group_message(group_id, [info_msg])

            elif cmd == "members":
                member_list = await self.group_api.get_group_member_list(group_id)
                members = [f"{m['user_id']} ({m['nickname']})" for m in member_list['data']]
                members_str = "\n".join(members[:20])
                await self.message_api.send_group_message(group_id, [f"群成员（前20个）:\n{members_str}"])

            elif cmd == "kick":
                if len(msg) < 3 or not validate_qq(msg[2]):
                    await self._send_error(group_id, "使用方法: /group kick <QQ号>")
                    return
                await self.group_api.kick_group_member(group_id, msg[2])
                await self.message_api.send_group_message(group_id, [f"已踢出 {msg[2]}"])

            elif cmd == "setadmin":
                if len(msg) < 4 or not validate_qq(msg[2]) or msg[3].lower() not in ["true", "false"]:
                    await self._send_error(group_id, "使用方法: /group setadmin <QQ号> <true|false>")
                    return
                enable = msg[3].lower() == "true"
                await self.group_api.set_group_admin(group_id, msg[2], enable)
                action = "设置" if enable else "取消"
                await self.message_api.send_group_message(group_id, [f"已{action} {msg[2]} 的管理员权限"])

            elif cmd == "setname":
                if len(msg) < 3:
                    await self._send_error(group_id, "使用方法: /group setname <新群名>")
                    return
                new_name = " ".join(msg[2:])
                await self.group_api.set_group_name(group_id, new_name)
                await self.message_api.send_group_message(group_id, [f"群名已修改为 {new_name}"])

            elif cmd == "settitle":
                if len(msg) < 4 or not validate_qq(msg[2]):
                    await self._send_error(group_id, "使用方法: /group settitle <QQ号> <头衔>")
                    return
                title = " ".join(msg[3:])
                await self.group_api.set_group_special_title(group_id, msg[2], title)
                await self.message_api.send_group_message(group_id, [f"已为 {msg[2]} 设置头衔: {title}"])

            elif cmd == "atallcount":
                at_all_info = await self.group_api.get_group_at_all_remain(group_id)
                remain = at_all_info.get('data', {}).get('remain', 0)
                await self.message_api.send_group_message(group_id, [f"群@全体剩余次数: {remain}"])

            elif cmd == "mutelist":
                mute_list = await self.group_api.get_group_mute_list(group_id)
                muted = [f"{m['user_id']} ({m['nickname']})" for m in mute_list['data'] if m['shut_up_timestamp'] > 0]
                mute_str = "\n".join(muted[:20]) if muted else "无禁言成员"
                await self.message_api.send_group_message(group_id, [f"群禁言列表（前20个）:\n{mute_str}"])

            elif cmd == "poke":
                if len(msg) < 3 or not validate_qq(msg[2]):
                    await self._send_error(group_id, "使用方法: /group poke <QQ号>")
                    return
                await self.group_api.send_group_poke(group_id, msg[2])
                await self.message_api.send_group_message(group_id, [f"已戳一戳 {msg[2]}"])

            elif cmd == "like":
                if len(msg) < 4 or not validate_qq(msg[2]) or not msg[3].isdigit():
                    await self._send_error(group_id, "使用方法: /group like <QQ号> <次数>")
                    return
                times = int(msg[3])
                await self.group_api.send_like(msg[2], times)
                await self.message_api.send_group_message(group_id, [f"已为 {msg[2]} 点赞 {times} 次"])

            elif cmd == "sendimg":
                if len(msg) < 3 or not validate_url(msg[2]):
                    await self._send_error(group_id, "使用方法: /group sendimg <图片URL>")
                    return
                await self.message_api.send_group_image(group_id, msg[2])
                await self.message_api.send_group_message(group_id, ["图片已发送"])

            elif cmd == "sendvoice":
                if len(msg) < 3 or not validate_url(msg[2]):
                    await self._send_error(group_id, "使用方法: /group sendvoice <语音URL>")
                    return
                await self.message_api.send_group_voice(group_id, msg[2])
                await self.message_api.send_group_message(group_id, ["语音已发送"])

            elif cmd == "sendjson":
                if len(msg) < 3:
                    await self._send_error(group_id, "使用方法: /group sendjson <JSON内容>")
                    return
                json_content = " ".join(msg[2:])
                await self.message_api.send_group_json(group_id, json_content)
                await self.message_api.send_group_message(group_id, ["JSON消息已发送"])

            elif cmd == "reply":
                if len(msg) < 4:
                    await self._send_error(group_id, "使用方法: /group reply <消息ID> <内容>")
                    return
                message_id, content = msg[2], " ".join(msg[3:])
                await self.message_api.send_group_reply(group_id, message_id, content)
                await self.message_api.send_group_message(group_id, ["回复消息已发送"])

            elif cmd == "recall":
                if len(msg) < 3:
                    await self._send_error(group_id, "使用方法: /group recall <消息ID>")
                    return
                await self.message_api.recall_group_message(group_id, msg[2])
                await self.message_api.send_group_message(group_id, ["消息已撤回"])

            elif cmd == "movefile":
                if len(msg) < 4:
                    await self._send_error(group_id, "使用方法: /group movefile <文件ID> <目标目录>")
                    return
                await self.group_api.move_group_file(group_id, msg[2], msg[3])
                await self.message_api.send_group_message(group_id, ["群文件已移动"])

            elif cmd == "uploadfile":
                if len(msg) < 3 or not validate_url(msg[2]):
                    await self._send_error(group_id, "使用方法: /group uploadfile <文件URL>")
                    return
                await self.group_api.upload_group_file(group_id, msg[2])
                await self.message_api.send_group_message(group_id, ["群文件已上传"])

            elif cmd == "ocr":
                if len(msg) < 3 or not validate_url(msg[2]):
                    await self._send_error(group_id, "使用方法: /group ocr <图片URL>")
                    return
                ocr_result = await self.message_api.ocr_image(msg[2])
                await self.message_api.send_group_message(group_id, [f"OCR识别结果:\n{ocr_result}"])

            elif cmd == "typing":
                await self.group_api.set_typing_status(group_id)
                await self.message_api.send_group_message(group_id, ["已设置输入状态"])

            elif cmd == "sendtext":
                if len(msg) < 3:
                    await self._send_error(group_id, "使用方法: /group sendtext <内容>")
                    return
                content = " ".join(msg[2:])
                await self.message_api.send_group_text(group_id, content)
                await self.message_api.send_group_message(group_id, ["文本消息已发送"])

            elif cmd == "setwelcome":
                if len(msg) < 3:
                    await self._send_error(group_id, "使用方法: /group setwelcome <内容>")
                    return
                content = " ".join(msg[2:])
                await self.group_api.set_welcome_message(group_id, content)
                await self.message_api.send_group_message(group_id, ["入群欢迎消息已设置"])

            else:
                supported = (
                    "help, atall, mute, unmute, announce, essence, info, members, kick, setadmin, "
                    "setname, settitle, atallcount, mutelist, poke, like, sendimg, sendvoice, "
                    "sendjson, reply, recall, movefile, uploadfile, ocr, typing, sendtext, setwelcome"
                )
                await self._send_error(group_id, f"未知命令。支持: {supported}")

        except Exception as e:
            await self._send_error(group_id, f"命令执行失败: {str(e)}")

    @handler(GroupCommandSent)
    async def handle_group_request_command(self, ctx: EventContext):
        event = ctx.event
        if not event or not event.is_admin:
            return

        msg = event.text_message.strip().lower().split()
        group_id = str(event.launcher_id)
        if len(msg) < 4 or msg[0] != "/group" or msg[1] not in ["approve", "reject"]:
            return

        try:
            cmd, target_qq, flag = msg[1], msg[2], msg[3]
            approve = cmd == "approve"
            await self.group_api.handle_group_request(flag, approve)
            action = "通过" if approve else "拒绝"
            await self.message_api.send_group_message(group_id, [f"已{action} {target_qq} 的加群请求"])
        except Exception as e:
            await self._send_error(group_id, f"处理加群请求失败: {str(e)}")

    def __del__(self):
        self.logger.info("GroupManagerPlugin unloaded")