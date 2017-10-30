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
    instances = instances[0]
    time.sleep(4)
    instances.reload()
    print("Dns name is: ", instances.public_dns_name)
    print ("*************************")


    # global dns_name
    # dns_name = instances[0].public_dns_name

    print ("Please wait while we ssh into the new instance")
    print ("*************************")
    cmd_ssh = ("ssh -t -o StrictHostKeyChecking=no -i rachel_lawton_dev.pem ec2-user@" + instances.public_dns_name + " 'sudo pwd'")
    time.sleep(60)
    (status, output) = subprocess.getstatusoutput(cmd_ssh)
    print ("status", status)
    print ("output" + output)
    if status > 0:
        print ("ssh to instance was not successful")
    else:
        print ("ssh to instancewas successful")

    #return dns_name



#def copyingCWS(dns_name):
    print ("Copying check_webserver file to new instance created using scp command")
    print ("*************************")
    cmd_scp = ("scp -i /Users/rachellawton/Amazon-web-server/rachel_lawton_dev.pem /Users/rachellawton/Amazon-web-server/check_webserver.py ec2-user@" + instances.public_dns_name +  ":.")
    time.sleep(20)
    #instances = instances[0]
    (status, output) = subprocess.getstatusoutput(cmd_scp)
    print ("status", status)
    print ("output" + output)
    if status > 0:
        print ("Copy to instance was not successful")
    else:
        print ("Copy to instance was successful")


    print ("*************************")
    print ("Making the file executable usng the chmod command")
    cmd_chmod = "ssh –i /Users/rachellawton/Amazon-web-server/rachel_lawton_dev.pem ec2-user@" + instances.public_dns_name + " 'chmod +x check_webserver.py'"
    # (status, output) = subprocess.getstatusoutput(cmd_chmod)
    # if status == 0:
    #     print ("File execution was not successful")
    # else:
    #     print ("File execution was successful")
    print ("*************************")
    print ("running the executed file ")
    cmd_runfile = "ssh –i /Users/rachellawton/Amazon-web-server/rachel_lawton_dev.pem ec2-user@" + instances.public_dns_name + " ./check_webserver.py"
    # (status, output) = subprocess.getstatusoutput(cmd_runfile)
    # if status == 0:
    #     print ("File was not successful")
    # else:
    #     print ("File was successful")

def checknginx():
    cmd = 'ps -A | grep nginx | grep -v grep'

    (status, output) = subprocess.getstatusoutput(cmd)

    if status > 0:  
        print("Nginx Server IS NOT running")
    else:
        print("Nginx Server IS running")



def create_bucket():
    print("Creating bucket please wait")
    print ("*************************")
    bucket_name = input("Please name your bucket:")
    try:
        response = s3.create_bucket(Bucket=bucket_name,CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})
        print ("bucket was created")
        print (response)
    except Exception as error:
        print (error)
        
    return response



def main():
    create_instances()
    #copyingCWS(dns_name)
    checknginx()
    create_bucket()
    

if __name__ == '__main__':
  main()



#instance.reload()     # ensures instance object has current live instance data

