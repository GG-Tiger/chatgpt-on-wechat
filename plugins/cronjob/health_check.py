from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.cron import CronTrigger

from channel.wechat.wechat_channel import WechatChannel
from common.log import logger
from plugins.cronjob import itchat_send
from plugins.cronjob.cron_job import CronJob


class HealthCheck(CronJob):
    def __init__(self, chan: WechatChannel):
        super(HealthCheck, self).__init__(chan)

    def run(self):
        logger.debug("start to run HealthCheck...")
        chan = WechatChannel(self.channel)
        itchat_send.send_text(chan, '多 十三', "ping")

    def get_job_scheduler(self) -> BaseTrigger:
        trigger = CronTrigger(hour='*/5', timezone='Asia/Shanghai')
        return trigger
