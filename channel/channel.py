"""
Message sending channel abstract class
"""
import common.weather
from bridge.bridge import Bridge
from bridge.context import Context, ContextType
from bridge.reply import *


class Channel(object):
    NOT_SUPPORT_REPLYTYPE = [ReplyType.VOICE, ReplyType.IMAGE]

    def startup(self):
        """
        init channel
        """
        raise NotImplementedError

    def handle_text(self, msg):
        """
        process received msg
        :param msg: message object
        """
        raise NotImplementedError

    # 统一的发送函数，每个Channel自行实现，根据reply的type字段发送不同类型的消息
    def send(self, reply: Reply, context: Context):
        """
        send message to user
        :param msg: message content
        :param receiver: receiver channel account
        :return:
        """
        raise NotImplementedError

    def build_reply_content(self, query, context: Context = None) -> Reply:
        return Bridge().fetch_reply_content(query, context)

    def build_voice_to_text(self, voice_file) -> Reply:
        return Bridge().fetch_voice_to_text(voice_file)

    def build_text_to_voice(self, text) -> Reply:
        return Bridge().fetch_text_to_voice(text)

    def build_current_weather(self, user_id: str) -> (Reply, Context):
        yes, wea = common.weather.get_latest_weather()
        rep = Reply()
        ctx = Context()
        kargs = dict()
        kargs['isgroup'] = False
        kargs['msg'] = False
        kargs['origin_ctype'] = ContextType.TEXT
        kargs['session_id'] = False
        kargs['receiver'] = user_id

        if yes:
            rep.type = ReplyType.TEXT
            rep.content = wea

            ctx.type = ContextType.TEXT
            ctx.content = wea
        else:
            rep.type = ReplyType.TEXT
            rep.content = "build reply error"

            ctx.type = ContextType.TEXT
            ctx.content = "build reply error"
        ctx.kwargs = kargs
        return rep, ctx
