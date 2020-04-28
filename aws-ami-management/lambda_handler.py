# ami_creation.py

from datetime import datetime, timedelta
import os
import boto3
import logging

RETENTION = os.getenv('RETENTION', 100)
# set logging
log = logging.getLogger()
log.setLevel(logging.DEBUG)
logging.getLogger('botocore').setLevel(logging.WARNING)

def get_session(region):
    return boto3.session.Session(region_name=region)


def get_instance_name(fid):
    ec2 = boto3.resource('ec2')
    ec2instance = ec2.Instance(fid)
    instancename = ''
    for tags in ec2instance.tags:
        if tags["Key"] == 'Name':
            instancename = tags["Value"]
    return instancename


def cleanup(region_id=REGION):
    '''This method searches for all AMI images with a tag of RemoveOn
       and a value of YYYYMMDD of the day its ran on then removes it
    '''
    today = datetime.utcnow().strftime('%Y%m%d')
    session = get_session(region_id)
    client = session.client('ec2')
    resource = session.resource('ec2')
    images = client.describe_images(Filters=[{'Name': 'tag:RemoveOn', 'Values': [today]}])
    for image_data in images['Images']:
        image = resource.Image(image_data['ImageId'])
        name_tag = [tag['Value'] for tag in image.tags if tag['Key'] == 'Name']
        if name_tag:
            print(f"Deregistering {name_tag[0]}")
        image.deregister()


def backup(region_id=REGION):
    '''This function searches for all EC2 instances with a tag of BackUp
       and creates a AMI for them and tags the images with a
       RemoveOn tag of a YYYYMMDD value of days in UTC mentioned in RETENTION variable from today
    '''
    created_on = datetime.utcnow().strftime('%Y%m%d')
    remove_on = (datetime.utcnow() + timedelta(days=RETENTION)).strftime('%Y%m%d')
    session = get_session(region_id)
    
    client = session.client('ec2')
    resource = session.resource('ec2')
    
    reservations = client.describe_instances(Filters=[{'Name': 'tag-key', 'Values': ['BackUp']}])
    
    for reservation in reservations['Reservations']:
        for instance_description in reservation['Instances']:
            instance_id = instance_description['InstanceId']
            name_tag = get_instance_name(instance_id)
            name = f"{name_tag}_InstanceId({instance_id})_CreatedOn({created_on})"
            print(f"Creating Backup: {name}")
            image_description = client.create_image(InstanceId=instance_id, Name=name, NoReboot=True)
            images = []
            images.append(image_description['ImageId'])
            image = resource.Image(image_description['ImageId'])
            image.create_tags(Tags=[{'Key': 'RemoveOn', 'Value': remove_on}, {'Key': 'Name', 'Value': name}])


def lambda_handler(event, context):
    '''This function acts as the handler for the lambda function to take backup of EC2 instances 
       with a tag of BackUp and creates a AMI for them and tags the images with a
       RemoveOn tag of a YYYYMMDD value of days in UTC mentioned in RETENTION environment
       variable from today
    '''
    log.info("Running AMI BACKUP CREATION")
    region = context.invoked_function_arn.split(':')[3]
    account_id = context.invoked_function_arn.split(':')[4]
    backup(region)
    log.info("AMI BACKUP CREATION successful")
    log.info("Running AMI BACKUP CLEANUP")
    cleanup(region)
    log.info("AMI BACKUP CLEANUP successful")
    return { 
        'message' : 'OK'
    }
