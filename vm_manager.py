import time
import paramiko
import os

class vm_conn:

    def __init__(self,vm,resource,user,password,ip):
        self.vm = vm
        self.resource = resource
        self.user = user
        self.password = password
        self.ip = ip
        command = "az vm start --name {} --resource-group {}".format(vm,resource)
        os.system(command)
        while True:
            try:
                self.run_script("ls",timeout=2,echo=False)
                break
            except:
                print("-", end="")
                time.sleep(2)

    def close_connnection(self):
        command = "az vm deallocate --name {} --resource-group {}".format(self.vm,self.resource)
        os.system(command)

    def run_script(self,script,timeout = 10,echo=True):
        if(echo):
            print("executing: " + script)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, username=self.user, password=self.password,timeout=timeout)
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(script)
        out = ssh_stdout.read().decode('ascii').strip("\n")
        if(echo):
            print(out)