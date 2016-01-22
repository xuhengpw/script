# #!/usr/bin/python
# import paramiko
# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect(“某IP地址”,22,”用户名”, “口令”)
# stdin, stdout, stderr = ssh.exec_command(“你的命令”)
# print stdout.readlines()
# ssh.close()