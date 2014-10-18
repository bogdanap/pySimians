import re
from collections import defaultdict
from subprocess import check_output
import ConfigParser


class GCEMixin(object):
    """ A basic plugin to interact with Google Compute Engine"""
    def __init__(self):
        super(GCEMixin, self).__init__()
        self._cge_machines = None
        self._gce_enabled = False
        if self.config.has_section("gce"):
            self._gce_enabled = True #bool(self.config.get("gce", "enabled"))
            self._gce_pattern = self.config.get("gce", "pattern")

    def get_vm_groups(self):
        super_groups = super(GCEMixin, self).get_vm_groups()
        if self._gce_enabled:
            output = check_output("gcloud compute instances list".split())
            for lines in output[1:]:
                name, zone, _, _, external_ip, status = line.split()
                if status == "RUNNING" and re.match(self._gce_pattern):
                    super_groups["gce"].append(external_ip)
        return super_groups


class Monkey(GCEmixin, object):
# Superclass for all monkey types

    def __init__(self, config, scheduler):
        self.config = config
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
