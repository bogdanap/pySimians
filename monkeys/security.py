from supermonkey import Monkey


class SecurityMonkey(Monkey):

    def __init__(self, config_file, scheduler):
        super(SecurityMonkey, self).__init__(config_file, scheduler)
        schedule = self.config.items('security_schedule')
        int_schedule = map(lambda (x, y): (x, int(y)), schedule)
        self.scheduler.add_job(self.time_of_the_monkey, trigger='interval',
                               **dict(int_schedule))
