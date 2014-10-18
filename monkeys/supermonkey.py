import ConfigParser

from collections import defaultdict


class Monkey(object):
# Superclass for all monkey types

    def __init__(self, config_file, scheduler):
        self.config = ConfigParser.RawConfigParser(allow_no_value=True)
        self.config.read(config_file)
        self.scheduler = scheduler

    def get_vm_groups(self):
        groups = defaultdict(list)
        for vm in self.config.items("vms"):
            ip, labels = vm
            if not labels:
                labels = "no_label"
            for label in labels.split(","):
                groups[label].append(ip)
        return groups

    def get_all_ips(self):
        return [ip for ip, _ in self.config.items("vms")]

    def time_of_the_monkey(self):
        raise NotImplemented
