import datetime
import os
import random

from scriptrunner import ScriptRunner
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

        self.username = None
        self.password = None
        self.key_filename = None
        if self.config.has_option("vms_authentication", "username"):
          self.username = self.config.get("vms_authentication", "username")
        if self.config.has_option("vms_authentication", "password"):
          self.password = self.config.get("vms_authentication", "password")
        if self.config.has_option("vms_authentication", "key_filename"):
          self.key_filename = self.config.get("vms_authentication", "key_filename")
        self.last_run = None

    def load_chaos_scripts(self):
        self.SCRIPT_DIR = "../scripts/chaos_safe/"
        return [f for f in os.listdir(self.SCRIPT_DIR) if
                os.path.isfile(os.path.join(self.SCRIPT_DIR, f))]

    def time_of_the_monkey(self):
        """Create some chaos"""
        if not self.should_run():
            return
        chaos = random.choice(self.chaos_types)
        vm = random.choice(self.get_all_ips())
        runner = ScriptRunner(vm)
        runner.connect(username=self.username, password=self.password, key_filename=self.key_filename)
        runner.run_file(self.SCRIPT_DIR + "/" + chaos)
        runner.close()
        #TODO run bash script on vm
        self.last_run = datetime.datetime.now()

    def should_run(self):
        cooloff = int(self.config.get("chaos", "cooloff"))
        if self.last_run and datetime.datetime.now() - datetime.timedelta(
                hours=cooloff) < self.last_run:
            return False
        probability = float(self.config.get("chaos", "probability"))
        if random.random() > probability:
            return False
        return True
