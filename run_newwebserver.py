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
    print ("Succes an instance with ID", instances[0].id, "has been created.")
    print ("*************************")

def checknginx():
    cmd = 'ps -A | grep nginx | grep -v grep'

    (status, output) = subprocess.getstatusoutput(cmd)

    if status > 0:  
        print("Nginx Server IS NOT running")
    else:
        print("Nginx Server IS running")



def main():
    create_instances()
    checknginx()
if __name__ == '__main__':
  main()



#instance.reload()     # ensures instance object has current live instance data

