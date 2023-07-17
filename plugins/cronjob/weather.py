from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.cron import CronTrigger

from channel.wechat.wechat_channel import WechatChannel
from common.log import logger
from common.weather import get_latest_weather
from plugins.cronjob import itchat_send
from plugins.cronjob.cron_job import CronJob


class WeatherBroadcast(CronJob):
    def __init__(self, chan: WechatChannel):
        super(WeatherBroadcast, self).__init__(chan)

    def run(self):
        logger.debug("start to run Weather broadcast...")
        self._send_weather()

    def get_job_scheduler(self) -> BaseTrigger:
        # trigger = CronTrigger(hour='0-23', minute='0-59', second='0-59', timezone='Asia/Shanghai')
        trigger = CronTrigger(hour='9', minute='0', second='0', timezone='Asia/Shanghai')

        return trigger

    def _send_weather(self):
        chan = WechatChannel(self.channel)
        # user = itchat.search_friends(nickName='多 十三')
        # user = itchat.search_friends(nickName='G－bear')
        # logger.debug("itchat.search_friends,res:{}".format(user))
        yes, today_weather = get_latest_weather()
        if yes:
            itchat_send.send_text(chan, '多 十三', today_weather)
            itchat_send.send_text(chan, 'G－bear', today_weather)
        else:
            itchat_send.send_text(chan, '多 十三', "播报天气失败")
