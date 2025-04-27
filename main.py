from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *
from pkg.platform.types import *
import yaml
from plugins.GroupManagerPlugin.api.group import GroupAPI
from plugins.GroupManagerPlugin.api.message import MessageAPI

@register(name="GroupManagerPlugin", description="QQ群管理插件，支持多种群聊管理功能", version="0.4", author="YuWan_SAMA")
class GroupManagerPlugin(BasePlugin):
    def __init__(self, host: APIHost):
        super().__init__(host)
        self.ap = host
        # 初始化 API 模块
        self.group_api = GroupAPI(host="127.0.0.1", port=3000)
        self.message_api = MessageAPI(host="127.0.0.1", port=3000)
        # 加载配置文件
        self.config = self.load_config()

    def load_config(self) -> dict:
        """加载并验证配置文件"""
        default_config = {"admin": []}
        try:
            with open("settings.yaml", "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or default_config
                if not isinstance(data, dict):
                    print("配置文件格式错误，使用默认配置")
                    return default_config
                # 验证 admin 字段
                if "admin" not in data:
                    data["admin"] = []
                if not isinstance(data["admin"], list):
                    print("admin 字段必须为列表，使用默认配置")
                    data["admin"] = []
                # 确保 admin 列表中的元素是字符串
                data["admin"] = [str(item) for item in data["admin"]]
                return data
        except FileNotFoundError:
            print("配置文件不存在，使用默认配置")
            return default_config
        except Exception as e:
            print(f"加载配置文件失败: {str(e)}")
            return default_config

    async def initialize(self):
        # 插件初始化
        pass

    @handler(GroupMessageReceived)
    async def group_command_sent(self, ctx: EventContext):
        event = ctx.event
        msg = str(event.message_chain).strip()
        group_id = str(event.launcher_id)
        sender_id = int(event.sender_id)

        # 检查消息是否以 /group 开头
        if not msg.startswith("/group"):
            return

        # 验证管理员权限
        if sender_id not in self.config["admin"]:
            await self.message_api.send_group_message(group_id, MessageChain(["权限不足，仅管理员可执行指令"]))
            return

        command = msg.lower().split()
        if len(command) < 1:
            return

        if len(command) < 2:
            await self.message_api.send_group_message(group_id, MessageChain(["使用方法: /group [command] [参数]"]))
            return

        try:
            cmd = command[1]
            if cmd == "help":
                # 显示帮助信息
                help_text = (
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
                    "/group sendface <表情ID> - 发送系统表情\n"
                    "/group sendjson <JSON内容> - 发送JSON消息\n"
                    "/group reply <消息ID> <内容> - 回复消息\n"
                    "/group recall <消息ID> - 撤回消息\n"
                    "/group movefile <文件ID> <目标目录> - 移动群文件\n"
                    "/group uploadfile <文件URL> - 上传群文件\n"
                    "/group ocr <图片URL> - 图片OCR识别\n"
                    "/group typing - 设置输入状态\n"
                    "/group sendtext <内容> - 发送纯文本消息"
                )
                await self.message_api.send_group_message(group_id, MessageChain([help_text]))

            elif cmd == "atall":
                if len(command) < 3:
                    await self.message_api.send_group_message(group_id, MessageChain(["使用方法: /group atall <消息内容>"]))
                    return
                await self.message_api.send_group_message(group_id, MessageChain([
                    AtAll(),
                    Plain(" ".join(command[2:]))
                ]))

            elif cmd == "mute":
                if len(command) < 4:
                    await self.message_api.send_group_message(group_id, MessageChain(["使用方法: /group mute <QQ号> <分钟>"]))
                    return
                target_qq = command[2]
                duration = int(command[3]) * 60  # 转换为秒
                await self.group_api.mute_group_member(group_id, target_qq, duration)
                await self.message_api.send_group_message(group_id, MessageChain([f"已禁言 {target_qq} {command[3]}分钟"]))

            elif cmd == "unmute":
                if len(command) < 3:
                    await self.message_api.send_group_message(group_id, MessageChain(["使用方法: /group unmute <QQ号>"]))
                    return
                target_qq = command[2]
                await self.group_api.mute_group_member(group_id, target_qq, 0)
                await self.message_api.send_group_message(group_id, MessageChain([f"已解除 {target_qq} 的禁言"]))

            elif cmd == "announce":
                if len(command) < 3:
                    await self.message_api.send_group_message(group_id, MessageChain(["使用方法: /group announce <公告内容>"]))
                    return
                content = " ".join(command[2:])
                await self.group_api.send_group_notice(group_id, content)
                await self.message_api.send_group_message(group_id, MessageChain(["公告已发布"]))

            elif cmd == "essence":
                if len(command) < 3:
                    await self.message_api.send_group_message(group_id, MessageChain(["使用方法: /group essence <消息ID>"]))
                    return
                message_id = command[2]
                await self.group_api.set_essence_message(group_id, message_id)
                await self.message_api.send_group_message(group_id, MessageChain(["已设置群精华消息"]))

            elif cmd == "info":
                group_info = await self.group_api.get_group_info(group_id)
                info_msg = (
                    f"群ID: {group_info['group_id']}\n"
                    f"群名: {group_info['group_name']}\n"
                    f"成员数: {group_info['member_count']}\n"
                    f"最大成员数: {group_info['max_member_count']}"
                )
                await self.message_api.send_group_message(group_id, MessageChain([info_msg]))

            elif cmd == "members":
                member_list = await self.group_api.get_group_member_list(group_id)
                members = [f"{m['user_id']} ({m['nickname']})" for m in member_list['data']]
                members_str = "\n".join(members[:20])  # 限制显示前20个成员
                await self.message_api.send_group_message(group_id, MessageChain([f"群成员（前20个）:\n{members_str}"]))

            elif cmd == "kick":
                if len(command) < 3:
                    await self.message_api.send_group_message(group_id, MessageChain(["使用方法: /group kick <QQ号>"]))
                    return
                target_qq = command[2]
                await self.group_api.kick_group_member(group_id, target_qq)
                await self.message_api.send_group_message(group_id, MessageChain([f"已踢出 {target_qq}"]))

            elif cmd == "setadmin":
                if len(command) < 4:
                    await self.message_api.send_group_message(group_id, MessageChain(["使用方法: /group setadmin <QQ号> <true|false>"]))
                    return
                target_qq = command[2]
                enable = command[3].lower() == "true"
                await self.group_api.set_group_admin(group_id, target_qq, enable)
                action = "设置" if enable else "取消"
                await self.message_api.send_group_message(group_id, MessageChain([f"已{action} {target_qq} 的管理员权限"]))

            elif cmd == "setname":
                if len(command) < 3:
                    await self.message_api.send_group_message(group_id, MessageChain(["使用方法: /group setname <新群名>"]))
                    return
                new_name = " ".join(command[2:])
                await self.group_api.set_group_name(group_id, new_name)
                await self.message_api.send_group_message(group_id, MessageChain([f"群名已修改为 {new_name}"]))

            elif cmd == "settitle":
                if len(command) < 4:
                    await self.message_api.send_group_message(group_id, MessageChain(["使用方法: /group settitle <QQ号> <头衔>"]))
                    return
                target_qq = command[2]
                title = " ".join(command[3:])
                await self.group_api.set_group_special_title(group_id, target_qq, title)
                await self.message_api.send_group_message(group_id, MessageChain([f"已为 {target_qq} 设置头衔: {title}"]))

            elif cmd == "atallcount":
                at_all_info = await self.group_api.get_group_at_all_remain(group_id)
                remain = at_all_info.get('data', {}).get('remain', 0)
                await self.message_api.send_group_message(group_id, MessageChain([f"群@全体剩余次数: {remain}"]))

            elif cmd == "mutelist":
                mute_list = await self.group_api.get_group_mute_list(group_id)
                muted = [f"{m['user_id']} ({m['nickname']})" for m in mute_list['data'] if m['shut_up_timestamp'] > 0]
                mute_str = "\n".join(muted[:20]) if muted else "无禁言成员"
                await self.message_api.send_group_message(group_id, MessageChain([f"群禁言列表（前20个）:\n{mute_str}"]))

            elif cmd == "poke":
                if len(command) < 3:
                    await self.message_api.send_group_message(group_id, MessageChain(["使用方法: /group poke <QQ号>"]))
                    return
                target_qq = command[2]
                await self.group_api.send_group_poke(group_id, target_qq)
                await self.message_api.send_group_message(group_id, MessageChain([f"已戳一戳 {target_qq}"]))

            elif cmd == "like":
                if len(command) < 4:
                    await self.message_api.send_group_message(group_id, MessageChain(["使用方法: /group like <QQ号> <次数>"]))
                    return
                target_qq = command[2]
                times = int(command[3])
                await self.group_api.send_like(target_qq, times)
                await self.message_api.send_group_message(group_id, MessageChain([f"已为 {target_qq} 点赞 {times} 次"]))

            elif cmd == "sendimg":
                if len(command) < 3:
                    await self.message_api.send_group_message(group_id, MessageChain(["使用方法: /group sendimg <图片URL>"]))
                    return
                image_url = command[2]
                await self.message_api.send_group_image(group_id, image_url)
                await self.message_api.send_group_message(group_id, MessageChain(["图片已发送"]))

            elif cmd == "sendvoice":
                if len(command) < 3:
                    await self.message_api.send_group_message(group_id, MessageChain(["使用方法: /group sendvoice <语音URL>"]))
                    return
                voice_url = command[2]
                await self.message_api.send_group_voice(group_id, voice_url)
                await self.message_api.send_group_message(group_id, MessageChain(["语音已发送"]))

            elif cmd == "sendface":
                if len(command) < 3:
                    await self.message_api.send_group_message(group_id, MessageChain(["使用方法: /group sendface <表情ID>"]))
                    return
                face_id = command[2]
                await self.message_api.send_group_face(group_id, face_id)
                await self.message_api.send_group_message(group_id, MessageChain(["系统表情已发送"]))

            elif cmd == "sendjson":
                if len(command) < 3:
                    await self.message_api.send_group_message(group_id, MessageChain(["使用方法: /group sendjson <JSON内容>"]))
                    return
                json_content = " ".join(command[2:])
                await self.message_api.send_group_json(group_id, json_content)
                await self.message_api.send_group_message(group_id, MessageChain(["JSON消息已发送"]))

            elif cmd == "reply":
                if len(command) < 4:
                    await self.message_api.send_group_message(group_id, MessageChain(["使用方法: /group reply <消息ID> <内容>"]))
                    return
                message_id = command[2]
                content = " ".join(command[3:])
                await self.message_api.send_group_reply(group_id, message_id, content)
                await self.message_api.send_group_message(group_id, MessageChain(["回复消息已发送"]))

            elif cmd == "recall":
                if len(command) < 3:
                    await self.message_api.send_group_message(group_id, MessageChain(["使用方法: /group recall <消息ID>"]))
                    return
                message_id = command[2]
                await self.message_api.recall_group_message(group_id, message_id)
                await self.message_api.send_group_message(group_id, MessageChain(["消息已撤回"]))

            elif cmd == "movefile":
                if len(command) < 4:
                    await self.message_api.send_group_message(group_id, MessageChain(["使用方法: /group movefile <文件ID> <目标目录>"]))
                    return
                file_id = command[2]
                target_dir = command[3]
                await self.group_api.move_group_file(group_id, file_id, target_dir)
                await self.message_api.send_group_message(group_id, MessageChain(["群文件已移动"]))

            elif cmd == "uploadfile":
                if len(command) < 3:
                    await self.message_api.send_group_message(group_id, MessageChain(["使用方法: /group uploadfile <文件URL>"]))
                    return
                file_url = command[2]
                await self.group_api.upload_group_file(group_id, file_url)
                await self.message_api.send_group_message(group_id, MessageChain(["群文件已上传"]))

            elif cmd == "ocr":
                if len(command) < 3:
                    await self.message_api.send_group_message(group_id, MessageChain(["使用方法: /group ocr <图片URL>"]))
                    return
                image_url = command[2]
                ocr_result = await self.message_api.ocr_image(image_url)
                await self.message_api.send_group_message(group_id, MessageChain([f"OCR识别结果:\n{ocr_result}"]))

            elif cmd == "typing":
                await self.group_api.set_typing_status(group_id)
                await self.message_api.send_group_message(group_id, MessageChain(["已设置输入状态"]))

            elif cmd == "sendtext":
                if len(command) < 3:
                    await self.message_api.send_group_message(group_id, MessageChain(["使用方法: /group sendtext <内容>"]))
                    return
                content = " ".join(command[2:])
                await self.message_api.send_group_text(group_id, content)
                await self.message_api.send_group_message(group_id, MessageChain(["文本消息已发送"]))

            else:
                supported = (
                    "help, atall, mute, unmute, announce, essence, info, members, kick, setadmin, "
                    "setname, settitle, atallcount, mutelist, poke, like, sendimg, sendvoice, "
                    "sendface, sendjson, reply, recall, movefile, uploadfile, ocr, typing, sendtext"
                )
                await self.message_api.send_group_message(group_id, MessageChain([f"未知命令。支持: {supported}"]))

        except Exception as e:
            await self.message_api.send_group_message(group_id, MessageChain([f"错误: {str(e)}"]))

    def __del__(self):
        # 清理资源
        pass