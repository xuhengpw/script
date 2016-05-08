#encoding: utf-8
import paramiko

def runcmd(ip,user,passwd,cline):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip,username=user, password=passwd)
    print ip,user,passwd,cline
    stdin, stdout, stderr = ssh.exec_command(cline)
    return stdout.readlines()
    ssh.close()


if __name__ == '__main__':
    a = runcmd('121.127.234.12','root','sss!@#','ls -l ')
    print a