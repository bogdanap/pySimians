from datetime import datetime
import logging
import os.path

from supermonkey import Monkey

logger = logging.getLogger('security')


class SecurityMonkey(Monkey):

    CONFIG_SECTION = "security"

    def __init__(self, config, scheduler, tweet):
        super(SecurityMonkey, self).__init__(config, scheduler, tweet)
        if self.is_enabled():
            int_schedule = map(lambda (x, y): (x, int(y)), self.get_schedule())
            self.scheduler.add_job(self.time_of_the_monkey, trigger='interval',
                                   **dict(int_schedule))

    def time_of_the_monkey(self):
        logger.info('Starting security run')
        ips = self.get_all_ips()
        scripts = self.load_scripts()
        self.result_count = len(ips * len(scripts))
        self.results = []
        for ip in ips:
            for script in scripts:
                self.scheduler.add_job(self.one_check, args=(ip, script),
                                       next_run_time=datetime.now())

    def one_check(self, ip, script_file):
        return_code, stdout, stderr = self.run_script_on_host(ip, script_file)
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
