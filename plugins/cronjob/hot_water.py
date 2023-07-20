import datetime
import io

from PIL import Image
from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.cron import CronTrigger

from bridge.context import Context, ContextType
from bridge.reply import Reply, ReplyType
from channel.wechat.wechat_channel import WechatChannel
from common.log import logger
from lib import itchat
from plugins.cronjob.cron_job import CronJob

hour_list = [11, 12, 14, 15, 16, 17, 18, 22]
hour_img_map = {
    11: "./resources/drink_water/cup1.png",
    12: "./resources/drink_water/cup2.png",
    14: "./resources/drink_water/cup3.png",
    15: "./resources/drink_water/cup4.png",
    16: "./resources/drink_water/cup5.png",
    17: "./resources/drink_water/cup6.png",
    18: "./resources/drink_water/cup7.png",
    22: "./resources/drink_water/cup8.png",
}


def trigger_filter():
    if datetime.date.today().weekday() in [5, 6]:  # 5 代表周六，6 代表周日
        return False
    now = datetime.datetime.now()
    if now.hour not in hour_list:
        return False
    else:
        return True


class DrinkHotWater(CronJob):
    def __init__(self, chan: WechatChannel):
        super(DrinkHotWater, self).__init__(chan)

    def run(self):
        logger.debug("start to run DrinkHotWater...")
        if trigger_filter():
            self._send_drink_water()
        else:
            logger.debug("pass run. for current hour")

    def get_job_scheduler(self) -> BaseTrigger:
        trigger = CronTrigger(hour='11-22', minute='0', second='0', timezone='Asia/Shanghai')
        return trigger

    def _send_drink_water(self):
        chan = WechatChannel(self.channel)
        try:
            # user = itchat.search_friends(nickName='多 十三')
            user = itchat.search_friends(nickName='G－bear')
            user_lb = itchat.search_friends(nickName='多 十三')
            logger.debug("itchat.search_friends,res:{}".format(user))
        except:
            logger.debug("fail to search_friends, maybe not login")
            return

        # IMAGE
        # Open an image file
        hour = datetime.datetime.now().hour
        with Image.open(hour_img_map[hour]) as img:
            # Convert the image to bytes
            out = io.BytesIO()
            with io.BytesIO() as output:
                img.save(out, format="PNG")
                reply = Reply(content=out, type=ReplyType.IMAGE)
                kargs = dict()
                kargs['isgroup'] = False
                kargs['msg'] = False
                kargs['origin_ctype'] = ContextType.IMAGE
                kargs['session_id'] = False
                kargs['receiver'] = user[0]['UserName']

                context = Context(type=ContextType.IMAGE, content=out, kwargs=kargs)
                ret = chan.send(reply, context)
                logger.debug("_send_drink_water, reply:{}, context:{}, itchat res:{}".format(reply, context, ret))

                context.kwargs['receiver'] = user_lb[0]['UserName']
                ret = chan.send(reply, context)