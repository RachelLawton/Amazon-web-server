#!/usr/bin/env python3
import boto3
import time
import sys
import subprocess


ec2 = boto3.resource('ec2')
s3 = boto3.resource('s3')

def create_instances():

    instances = ec2.create_instances(
        ImageId='ami-c5062ba0',           # Change if not in Ireland region
        KeyName='rachel_lawton_dev',                # replace with your key name
        MinCount=1,
        MaxCount=1,
        SecurityGroupIds=['sg-939cfafb'], # replace with your security group ID
            UserData='''#!/bin/bash 
            yum -y install nginx
            service nginx start
            chkconfig nginx on''', 
        InstanceType='t2.micro')

    print ("Instance is being created")
    print ("*************************")
    time.sleep(5)
    print ("Success an instance with ID", instances[0].id, "has been created.")
    print ("*************************")
    print ("Getting DNS name from instance")
    print ("*************************")
    time.sleep(4)
    instances[0].reload()
    print("Dns name is: ", instances[0].public_dns_name)
    print ("*************************")


    print ("Please wait while we ssh into the new instance")
    print ("*************************")
    cmd_ssh = ("ssh -t -o StrictHostKeyChecking=no -i rachel_lawton_dev.pem ec2-user@" + instances[0].public_dns_name + " 'sudo pwd'")
    time.sleep(60)
    (status, output) = subprocess.getstatusoutput(cmd_ssh)
    print ("status", status)
    print ("output" + output)
    if status > 0:
        print ("ssh to instance was not successful")
    else:
        print ("ssh to instancewas successful")

   



# def copingCWS(public_dns_name):

    
#     print ("Copying check_webserver file to new instance created using scp command")
#     print ("*************************")
#     cmd_scp = ("scp -i /Users/rachellawton/Amazon-web-server/rachel_lawton_dev.pem check_webserver.py ec2-user@" + public_dns_name +  ":.")
#     time.sleep(20)
#     (status, output) = subprocess.getstatusoutput(cmd_scp)
#     print ("status", status)
#     print ("output" + output)
#     if status > 0:
#         print ("Copy to instance was not successful")
#     else:
#         print ("Copy to instancewas successful")




# def checknginx():
#     cmd = 'ps -A | grep nginx | grep -v grep'

#     (status, output) = subprocess.getstatusoutput(cmd)

#     if status > 0:  
#         print("Nginx Server IS NOT running")
#     else:
#         print("Nginx Server IS running")



def main():
    create_instances()
    #checknginx()
    #sshIntoInstance(instances)

if __name__ == '__main__':
  main()



#instance.reload()     # ensures instance object has current live instance data

