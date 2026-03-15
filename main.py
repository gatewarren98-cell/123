import re
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import At, Plain

@register("mention_first_only", "你的名字", "仅当@机器人在首位时才触发回复", "1.0.0")
class MentionFirstOnlyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    # 使用正则 ".*" 捕获所有文本消息进行逻辑判断
    @filter.regex(r".*")
    async def handle_mention_message(self, event: AstrMessageEvent):
        # 1. 确保消息对象存在且有组件内容
        if not event.message_obj or not event.message_obj.message:
            return

        # 获取消息链的第一个组件
        components = event.message_obj.message
        first_comp = components[0]

        # 2. 判断第一个组件是否为 At (艾特)
        if isinstance(first_comp, At):
            # 获取当前机器人的 ID (根据 AstrBot 版本可能是 event.bot_id 或 event.get_self_id())
            bot_id = str(getattr(event, 'bot_id', '')) or str(event.get_self_id())
            
            # 获取该 At 组件指向的目标 ID (AstrBot 通常用 qq 属性存储)
            target_id = str(getattr(first_comp, 'qq', ''))

            # 3. 如果首位 @ 的正是机器人自己
            if target_id == bot_id:
                
                # 提取去掉首位 @ 之后的纯文本内容，方便后续处理
                real_text = "".join(
                    [comp.text for comp in components if isinstance(comp, Plain)]
                ).strip()

                # ---- 在这里写你希望 bot 执行的反应逻辑 ----
                yield event.plain_result(f"✅ 检测到首位 @！你对我说的内容是：{real_text}")
                
            else:
                # 场景：首位是 @，但 @ 的是其他群成员
                pass
        else:
            # 场景：首位不是 @（例如开头是文字、图片等）
            pass
