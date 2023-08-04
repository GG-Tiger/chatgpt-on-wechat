from bridge.context import ContextType, Context
from bridge.reply import Reply, ReplyType
from channel.wechat.wechat_channel import WechatChannel
from common.log import logger
from lib import itchat


def send_text(channel: WechatChannel, name: str, msg: str, isGroup=False) -> (bool, str):
    chan = WechatChannel(channel)
    kargs = dict()
    if isGroup:
        user = itchat.search_chatrooms(name=name)
        logger.debug("itchat.search_chatrooms,res:{}".format(user))
        kargs['receiver'] = user[0]['UserName']
    else:
        user = itchat.search_friends(nickName=name)
        kargs['receiver'] = user[0]['UserName']
        logger.debug("itchat.search_friends,res:{}".format(user))
    reply = Reply(content=msg, type=ReplyType.TEXT)
    kargs['isgroup'] = isGroup
    kargs['msg'] = False
    kargs['origin_ctype'] = ContextType.TEXT
    kargs['session_id'] = False

    context = Context(type=ContextType.TEXT, content=msg, kwargs=kargs)
    ret = chan.send(reply, context)
    logger.debug("send_text, reply:{}, context:{}, itchat res:{}".format(reply, context, ret))
    return True, ""