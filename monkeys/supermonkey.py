import re
from collections import defaultdict
from subprocess import check_output


class GCEMixin(object):
    """ A basic plugin to interact with Google Compute Engine"""
    def __init__(self, *args, **kwargs):
        super(GCEMixin, self).__init__(*args, **kwargs)
        self._cge_machines = None
        self._gce_enabled = False
        if self.config.has_section("gce"):
            self._gce_enabled = True #bool(self.config.get("gce", "enabled"))
            self._gce_pattern = self.config.get("gce", "pattern")

    def get_all_ips(self):
        super_ips = super(GCEMixin, self).get_all_ips()
        if self._gce_enabled:
            output = check_output("gcloud compute instances list".split()).splitlines()
            for line in output[1:]:
                name, zone, _, _, external_ip, status = [el for el in line.split() if el]
                if status == "RUNNING" and re.match(self._gce_pattern, name) is not None:
                    super_ips.append(external_ip)
        return super_ips


class SuperMonkey(object):
# Superclass for all monkey types

    def __init__(self, config, scheduler, twitter):
        self.config = config
        self.scheduler = scheduler
        self.twitter = twitter

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


class Monkey(GCEMixin, SuperMonkey):
    pass
