# 获取指定模块中所有的类
import importlib
import inspect
import pkgutil
import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.base import BaseTrigger

import plugins
from channel.chat_channel import ChatChannel
from channel.wechat.wechat_channel import WechatChannel
from common.log import logger

Chat_Group_Name = "多多扭蛋家庭群"


class CronJob(object):
    def __init__(self, channel: ChatChannel):
        if type(channel) is not type(WechatChannel()):
            raise TypeError
        self.channel = channel

    def run_job(self):
        if not WechatChannel().online:
            logger.debug("pass cronjob run, for WechatChannel is not online")
            time.sleep(1)
        else:
            self.run()

    def run(self):
        raise NotImplementedError

    def get_job_scheduler(self) -> BaseTrigger:
        raise NotImplementedError


def get_classes(module):
    classes = []
    for name, obj in inspect.getmembers(module, inspect.isclass):
        classes.append(obj)
    return classes


# 获取指定类的所有子类
def get_subclasses():
    subclasses = []
    for _, modname, _ in pkgutil.walk_packages(plugins.cronjob.__path__):
        module = importlib.import_module(plugins.cronjob.__name__ + '.' + modname)
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, CronJob) and obj is not CronJob:
                subclasses.append(obj)
    logger.debug("cronjob all sub class:{}".format(subclasses))
    return subclasses


# 实例化所有子类并调用相应的方法
def run_subclasses(channel: ChatChannel):
    if type(channel) is not type(WechatChannel()):
        raise TypeError
    scheduler = BackgroundScheduler()
    for subclass in get_subclasses():
        instance = subclass(channel)
        logger.debug("instance:{}, add job. trigger:{}".format(instance.__class__, instance.get_job_scheduler()))
        scheduler.add_job(instance.run_job, instance.get_job_scheduler())
    scheduler.start()


def run_all_cronjob(channel: ChatChannel):
    if type(channel) is not type(WechatChannel()):
        logger.info(
            "pass cronjob threading, for current not wechat channel. current type:{}, need:{}".format(type(channel),
                                                                                                      WechatChannel))
        return
    logger.info("start to run all cronjob threading...")
    run_subclasses(channel)
