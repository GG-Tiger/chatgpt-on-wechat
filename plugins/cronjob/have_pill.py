import json
from datetime import datetime

from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.cron import CronTrigger

from channel.wechat.wechat_channel import WechatChannel
from common.log import logger
from lib import itchat
from plugins.cronjob import itchat_send
from plugins.cronjob.cron_job import CronJob, Chat_Group_Name


class HivePills(CronJob):
    def __init__(self, chan: WechatChannel):
        super(HivePills, self).__init__(chan)

    def run(self):
        logger.debug("start to run HivePills...")
        self._send_have_pill()

    def get_job_scheduler(self) -> BaseTrigger:
        # trigger = CronTrigger(second='*/5', timezone='Asia/Shanghai')
        trigger = CronTrigger(hour='23', minute='50', second='00', timezone='Asia/Shanghai')
        return trigger

    def _send_have_pill(self):
        chan = WechatChannel(self.channel)
        cur = datetime.now()
        msg = "现在是: {}点{}分\n 💗夫人该吃药了💗".format(cur.hour, cur.minute)

        itchat_send.send_text(chan, Chat_Group_Name, msg, True)

