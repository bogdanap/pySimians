import ConfigParser

from collections import defaultdict

class Monkey():
# Superclass for all monkey types

    def __init__(self):
        self.config = ConfigParser.RawConfigParser(allow_no_value=True)
        self.config.read("../monkey.config")

    def get_vm_groups(self):
        groups = defaultdict(list)
        for vm in self.config.items("vms"):
            ip, labels = vm
            for label in labels.split(","):
                groups[label].append(ip)
        return groups
