import argparse
import logging
import logging.config
import twitter

from apscheduler.schedulers.background import BlockingScheduler
import ConfigParser

from chaos import ChaosMonkey
from security import SecurityMonkey


log = logging.getLogger(__name__)

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
            m['class_name'](config_file, self.scheduler, self.tweet)

    def unleash(self):
        self.tweet("Unleashing the evil monkey horde...")
        self.scheduler.start()

    def get_twitter_connector(self):
        try:
            credentials = self.config_file.items("twitter")
        except ConfigParser.NoSectionError:
            return None
        return twitter.Api(**dict(credentials))

    def tweet(self, message):
      if not self.twitter:
        return
      try:
        self.twitter.PostUpdate(message)
      except Exception as e:
        log.exception(e)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Monkey runner')
    parser.add_argument('--config', default='../monkey.config',
                        dest='config_file', help='configuration file')
    args = parser.parse_args()
    config = ConfigParser.ConfigParser()
    config.read(args.config_file)
    logging.config.fileConfig(args.config_file)
    runner = MonkeyHorde(config)
    runner.unleash()
