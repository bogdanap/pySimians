import paramiko
import random
import os

class ScriptRunner(object):

  def __init__(self, host):
    self.host = host

  def connect(self, username=None, password=None, key_filename=None):
    self.client = paramiko.SSHClient()
    self.client.set_missing_host_key_policy(
          paramiko.AutoAddPolicy())
    self.client.connect(self.host, username=username, password=password, key_filename=key_filename)
    self.ftp = self.client.open_sftp()

  def run(self, command):
    stdin, stdout, stderr = self.client.exec_command(command)
    stdin.close()
    for line in stdout.read().splitlines():
      print 'host: %s: %s' % (self.host, line)
    return stdout.channel.recv_exit_status()

  def run_file(self, file_path):
    filename = os.path.basename(file_path)
    self.ftp.put(file_path, filename)
    command = "sh %s" %(filename)
    stdin, stdout, stderr = self.client.exec_command(command)
    self.ftp.remove(filename)
    return stdout.channel.recv_exit_status(), stdout.read(), stderr.read()

  def close(self):
    self.ftp.close()
    self.client.close()

if __name__=='__main__':
  runner = ScriptRunner('ec2-54-77-161-66.eu-west-1.compute.amazonaws.com')
  runner.connect(username='ubuntu')
  runner.run("uptime")

  # runner = ScriptRunner('127.0.0.1')
  # runner.connect(username='ioana', password='...')
  # runner.run('uptime')
  print runner.run_file('../scripts/chaos_safe/ls.sh')
