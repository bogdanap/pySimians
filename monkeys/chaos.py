import datetime
import os
import random

import cmd_runner
from supermonkey import Monkey

class ChaosMonkey(Monkey):

    def __init__(self, config_file, scheduler):
        super(ChaosMonkey, self).__init__(config_file, scheduler)
        is_enabled = bool(self.config.get("chaos", "enabled"))
        if is_enabled:
            schedule = self.config.items("chaos_schedule")
            scheduler.add_job(self.time_of_the_monkey, trigger='cron',
                              **dict(schedule))
        self.chaos_types = self.load_chaos_scripts()
        self.last_run = None

    def load_chaos_scripts(self):
        SCRIPT_DIR = "../scripts/"
        return [f for f in os.listdir(SCRIPT_DIR) if
                os.path.isfile(os.path.join(SCRIPT_DIR, f))]

    def time_of_the_monkey(self):
        """Create some chaos"""
        if not self.should_run():
            return
        chaos = random.choice(self.chaos_type)
        vm = random.choice(self.get_all_ips())
        #TODO run bash script on vm
        self.last_run = datetime.datetime.now()

    def should_run(self):
        cooloff = int(self.config.get("chaos", "cooloff"))
        if self.last_run and datetime.datetime.now() - datetime.timedelta(
                hours=cooloff) < self.last_run:
            return False
        return True

