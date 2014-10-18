#!/usr/bin/python

import paramiko
import cmd

class RunCommand(cmd.Cmd):
    """ Simple shell to run a command on the host """

    prompt = 'ssh > '

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.hosts = []
        self.connections = []

    def do_add_host(self, args):
        """add_host
        Add the host to the host list"""
        if args:
            self.hosts.append(args.split(','))
        else:
            print "usage: host "

    def do_connect(self, args):
        """Connect to all hosts in the hosts list"""
        for host in self.hosts:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())
            client.connect(host[0],
                username=host[1],
                password=host[2])
            self.connections.append(client)

    def do_run(self, command):
        """run
        Execute this command on all hosts in the list"""
        if command:
            for host, conn in zip(self.hosts, self.connections):
                stdin, stdout, stderr = conn.exec_command(command)
                stdin.close()
                for line in stdout.read().splitlines():
                    print 'host: %s: %s' % (host[0], line)
        else:
            print "usage: run "

    def do_close(self, args):
        for conn in self.connections:
            conn.close()

    def do_run_file(self, file):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.hosts[0][0],
                    username=self.hosts[0][1],
                    password=self.hosts[0][2])
        ftp = ssh.open_sftp()
        ftp.put(file, 'remotefile.sh')

        stdin, stdout, stderr = ssh.exec_command("sh remotefile.sh")
        for line in stdout.read().splitlines():
            print line
        ftp.close()
        ssh.close()

if __name__ == '__main__':
    RunCommand().cmdloop()
