import paramiko

class ScriptRunner(object):

  def __init__(self, host):
    self.host = host

  def connect(self, username=None, password=None, key_filename=None):
    self.client = paramiko.SSHClient()
    self.client.set_missing_host_key_policy(
          paramiko.AutoAddPolicy())
    self.client.connect(self.host, username=username, password=password, key_filename=key_filename)

  def run(self, command):
    stdin, stdout, stderr = self.client.exec_command(command)
    stdin.close()
    for line in stdout.read().splitlines():
      print 'host: %s: %s' % (self.host, line)

  def run_file(self, file_path):
    ftp = self.client.open_sftp()
    ftp.put(file_path, 'py_simian.sh')
    stdin, stdout, stderr = self.client.exec_command('sh py_simian.sh')
    for line in stdout.read().splitlines():
      print line
    ftp.close()
    self.client.close()

if __name__=='__main__':
  runner = ScriptRunner('ec2-54-77-161-66.eu-west-1.compute.amazonaws.com')
  runner.connect(username='ubuntu')
  runner.run("uptime")

  # runner = ScriptRunner('127.0.0.1')
  # runner.connect(username='ioana', password='...')
  # runner.run('uptime')
  runner.run_file('/Users/ioana/Documents/pySimians/scripts/ls.sh')