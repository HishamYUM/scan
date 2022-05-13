import paramiko
import getpass

import telnetlib
from telnetlib import Telnet


def startssh(host, user, passwd):#, commands):
 

    ssh_client = paramiko.SSHClient()

    # Must set the Host key policy as we haven't got the SSH key stored in Known Hosts
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


    ssh_client.connect(hostname=host,
                       username=user,
                       password=passwd)


    print("You Are Connected to: ", host)
    return ssh_client



print("Welcome to remote Switch configuration:")
print("Please Choose a Methode To Login:")
print("1 SSH\n2 Telnet")

choice = input('> ')

# commands = ["show mac address-table dynamic", "show IP arp", "show version"]
commands = ["sudo -S apt-get check ", "pwd", "ifconfig"]
######### SSH #########
if choice == "1":
    host = input("Please Enter The Hostname or IP address: ")
    username = input("Please Enter The Username: ")
    password = getpass.getpass()
    try:
        ssh_client = startssh(host, username, password)
        print("Executing Commands... \n")
        
        #create a csv file and write results to it
        output = open('terminaloutput.csv', 'w', encoding='utf-8')
        stdin, stdout, stderr = ssh_client.exec_command("-S enable")
        stdin.write("cisco\n")
        stdin.flush()
        outputstring = stdout.read()
        erroout = stderr.read()
        print(outputstring.decode())
        output.write(outputstring.decode())
        output.write(erroout.decode())
        output.write('\n')
        for command  in commands:
            
                stdin, stdout, stderr = ssh_client.exec_command(command)
                
                outputstring = stdout.read()
                erroout = stderr.read()
                print(outputstring.decode())
                output.write(outputstring.decode())
                output.write(erroout.decode())
                output.write('\n')
        ssh_client.close()

    except Exception as error:
        print ('\n Authentication Failed Or Connection Error To Host ' + host)
        print(error)
        exit(1)
    else:
        print ('Actions Completed Without Errors')

######### Telnet #########
elif choice == "2":

    tn = telnetlib.Telnet()

    host = "192.168.56.101"#input("Please Enter The Hostname or IP address: ")
    username = "kali"#input("Please Enter The Username: ")
    password = getpass.getpass()
    tn.open(host, port=23)

    tn.read_until(b"login: ", 5)
    tn.write(username.encode('ascii') + b"\n")
    if password:
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")
        
    print("Executing Commands Now.. \n")

    output = open('terminaloutput.csv', 'w', encoding='utf-8')
    for command in commands:
        
        
            command += "\n"
            tn.write(command.encode('utf-8'))
    tn.write(b"exit\n")
    # print(tn.read_very_eager().decode('ascii'))
    output.write(tn.read_all().decode())
    print("Finished!")
    

else: 
    print("Please Enter A Valid Choice")


