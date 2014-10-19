
from datetime import datetime
import logging
import os.path

from scriptrunner import ScriptRunner
from supermonkey import Monkey

logger = logging.getLogger('security')


class SecurityMonkey(Monkey):

    def __init__(self, config, scheduler, twitter):
        super(SecurityMonkey, self).__init__(config, scheduler, twitter)
        schedule = self.config.items('security_schedule')
        int_schedule = map(lambda (x, y): (x, int(y)), schedule)
        self.scheduler.add_job(self.time_of_the_monkey, trigger='interval',
                               **dict(int_schedule))
        self.username = None
        self.password = None
        self.key_filename = None
        if self.config.has_option("vms_authentication", "username"):
          self.username = self.config.get("vms_authentication", "username")
        if self.config.has_option("vms_authentication", "password"):
          self.password = self.config.get("vms_authentication", "password")
        if self.config.has_option("vms_authentication", "key_filename"):
          self.key_filename = self.config.get("vms_authentication", "key_filename")

    def time_of_the_monkey(self):
        logger.info('Security run')
        scripts = self.config.get('security', 'scripts')
        scripts = scripts.split(',')
        script_path = self.config.get('security', 'script_path')
        ips = self.get_all_ips()
        self.result_count = len(ips * len(scripts))
        self.results = []
        for ip in ips:
            for script_file in scripts:
                script = os.path.join(script_path, script_file)
                self.scheduler.add_job(self.one_check, args=(ip, script),
                                       next_run_time=datetime.now())

    def one_check(self, ip, script_file):
        runner = ScriptRunner(ip)
        runner.connect(username=self.username, password=self.password, key_filename=self.key_filename)
        return_code, stdout, stderr = runner.run_file(script_file)
        self.results.append(
            dict(return_code=return_code,
                 stdout=stdout,
                 stderr=stderr,
                 ip=ip,
                 scriptfile=script_file
                 )
        )
        self.result_count -= 1
        if not self.result_count:
            logger.info('Security run done. Check report')
            self.complete_run()
        runner.close()

    def complete_run(self):
        report_path = self.config.get('security', 'report_path')
        filename = 'security-report-%s.txt' % str(datetime.now())
        filename = os.path.join(report_path, filename)
        with open(filename, 'w') as f:
            for result in self.results:
                if not result['return_code'] and result['stdout'].strip() == 'OK':
                    f.write('%s - %s: OK\n' % (result['ip'],
                        result['scriptfile']))
                else:
                    f.write('%s - %s: (%s, %s)\n' % (result['ip'],
                        result['scriptfile'], result['stdout'],
                        result['stderr']))
