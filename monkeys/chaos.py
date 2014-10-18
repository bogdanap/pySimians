import os
from supermonkey import Monkey

class ChaosMonkey(Monkey):

    def __init__(self, config_file, scheduler):
        super(ChaosMonkey, self).__init__(config_file, scheduler)
        self.chaos_types = self.load_chaos_scripts()

    def load_chaos_scripts(self):
        SCRIPT_DIR = "../scripts/"
        return [f for f in os.listdir(SCRIPT_DIR) if
                os.path.isfile(os.path.join(SCRIPT_DIR, f))]

    def unleash(self):
        pass

    def should_run(self):
        pass

