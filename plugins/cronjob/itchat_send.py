from bridge.context import ContextType, Context
from bridge.reply import Reply, ReplyType
from channel.wechat.wechat_channel import WechatChannel
from common.log import logger
from lib import itchat


def send_text(channel: WechatChannel, wechat_nick_name: str, msg: str) -> (bool, str):
    chan = WechatChannel(channel)
    # try:
    #     # user = itchat.search_friends(nickName='多 十三')
    #     user = itchat.search_friends(nickName=wechat_nick_name)
    #     logger.debug("itchat.search_friends,res:{}".format(user))
    #     reply = Reply(content=msg, type=ReplyType.TEXT)
    #     kargs = dict()
    #     kargs['isgroup'] = False
    #     kargs['msg'] = False
    #     kargs['origin_ctype'] = ContextType.TEXT
    #     kargs['session_id'] = False
    #     kargs['receiver'] = user[0]['UserName']
    #
    #     context = Context(type=ContextType.TEXT, content=msg, kwargs=kargs)
    #     ret = chan.send(reply, context)
    #     logger.debug("send_text, reply:{}, context:{}, itchat res:{}".format(reply, context, ret))
    #     return True, ""
    # except:
    #     logger.debug("fail to search_friends, maybe not login")
    #     return False, "fail to search_friends, maybe not login"
    # user = itchat.search_friends(nickName='多 十三')
    user = itchat.search_friends(nickName=wechat_nick_name)
    logger.debug("itchat.search_friends,res:{}".format(user))
    reply = Reply(content=msg, type=ReplyType.TEXT)
    kargs = dict()
    kargs['isgroup'] = False
    kargs['msg'] = False
    kargs['origin_ctype'] = ContextType.TEXT
    kargs['session_id'] = False
    kargs['receiver'] = user[0]['UserName']

    context = Context(type=ContextType.TEXT, content=msg, kwargs=kargs)
    ret = chan.send(reply, context)
    logger.debug("send_text, reply:{}, context:{}, itchat res:{}".format(reply, context, ret))
    return True, ""