
from apscheduler.schedulers.background import BlockingScheduler

from chaos import ChaosMonkey
#from janitor import JanitorMonkey
from security import SecurityMonkey


class MonkeyHorde(object):

    def __init__(self, config_file):
        self.config_file = config_file
        self.monkey_list = [
            dict(class_name=ChaosMonkey),
            dict(class_name=SecurityMonkey),
        ]
        self.scheduler = BlockingScheduler()
        for m in self.monkey_list:
            m['class_name'](config_file, self.scheduler)

    def unleash(self):
        self.scheduler.start()
