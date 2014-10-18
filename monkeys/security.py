from supermonkey import Monkey

class SecurityMonkey(Monkey):

    def __init__(self, config_file, scheduler):
        super(SecurityMonkey, self).__init__(config_file, scheduler)
