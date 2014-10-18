
import logging

from supermonkey import Monkey

logger = logging.getLogger('security')

class SecurityMonkey(Monkey):

    def __init__(self, config, scheduler):
        super(SecurityMonkey, self).__init__(config, scheduler)
        schedule = self.config.items('security_schedule')
        int_schedule = map(lambda (x, y): (x, int(y)), schedule)
        self.scheduler.add_job(self.time_of_the_monkey, trigger='interval',
                **dict(int_schedule))

    def time_of_the_monkey(self):
        logger.warn("*" * 80)
