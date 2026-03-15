from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import At, Plain
from astrbot.api import logger

@register("mention_first_only", "开发者", "仅当@机器人在首位时才触发", "1.1.0")
class MentionFirstOnlyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    # 捕获所有文本消息
    @filter.regex(r".*")
    async def handle_mention_message(self, event: AstrMessageEvent):
        # 如果消息为空，直接忽略
        if not event.message_obj or not event.message_obj.message:
            return

        components = event.message_obj.message
        
        # 1. 过滤掉开头无意义的空白字符，找到真正的“第一个”有效组件
        first_valid_comp = None
        valid_start_index = 0
        
        for i, comp in enumerate(components):
            if isinstance(comp, Plain) and not comp.text.strip():
                # 如果是纯文本且去空格后是空的，跳过
                continue
            first_valid_comp = comp
            valid_start_index = i
            break

        if not first_valid_comp:
            return

        # 2. 判断这第一个有效组件是不是 At
        if isinstance(first_valid_comp, At):
            # 兼容不同版本的获取 ID 方式
            bot_id = str(event.get_self_id())
            # 兼容不同平台的 At 目标 ID 字段 (qq, target_id 等)
            target_id = str(getattr(first_valid_comp, 'qq', getattr(first_valid_comp, 'target', '')))

            # 3. 如果首位 @ 的是机器人自己
            if target_id == bot_id:
                # 提取去掉首位 @ 之后的纯文本内容
                real_text = "".join(
                    [comp.text for comp in components[valid_start_index + 1:] if isinstance(comp, Plain)]
                ).strip()

                # 测试用的回复
                yield event.plain_result(f"✅ 成功触发！检测到首位 @，你说的内容是：{real_text}")
                
            else:
                # 如果你需要在后台看为什么没触发，可以取消下面这行的注释
                # logger.info(f"[调试] 首位是@，但目标是 {target_id}，本机是 {bot_id}")
                pass
        else:
            # logger.info(f"[调试] 首位有效组件不是 At，而是 {type(first_valid_comp)}")
            pass
