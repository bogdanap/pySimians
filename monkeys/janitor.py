from supermonkey import Monkey

class JanitorMonkey(Monkey):

    def __init__(self, config_file, scheduler):
        super(JanitorMonkey, self).__init__(config_file, scheduler)
