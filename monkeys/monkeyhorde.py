import ConfigParser
import twitter
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
        self.twitter = self.get_twitter_connector()
        self.scheduler = BlockingScheduler()
        for m in self.monkey_list:
            m['class_name'](config_file, self.scheduler, self.twitter)

    def unleash(self):
        if self.twitter:
            self.twitter.PostUpdate("I unleashed the evil monkey horde!!!")
        self.scheduler.start()

    def get_twitter_connector(self):
        try:
            credentials = self.config_file.items("twitter")
        except ConfigParser.NoSectionError:
            return None
        return twitter.Api(**dict(credentials))

