# ami_creation.py

from datetime import datetime, timedelta
import aws_utils as awsutils
import os
import boto3

REGION = os.environ['AWS_REGION']
RETENTION = os.getenv('RETENTION', 1)

def get_instance_name(fid):
    # When given an instance ID as str e.g. 'i-1234567', return the instance 'Name' from the name tag.
    ec2 = boto3.resource('ec2')
    ec2instance = ec2.Instance(fid)
    instancename = ''
    for tags in ec2instance.tags:
        if tags["Key"] == 'Name':
            instancename = tags["Value"]
    return instancename

def backup(region_id=REGION):
    '''This function searches for all EC2 instances with a tag of BackUp
       and creates a AMI for them and tags the images with a
       RemoveOn tag of a YYYYMMDD value of days in UTC mentioned in RETENTION variable from today
    '''
    created_on = datetime.utcnow().strftime('%Y%m%d')
    remove_on = (datetime.utcnow() + timedelta(days=RETENTION)).strftime('%Y%m%d')
    session = awsutils.get_session(region_id)
    
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

if __name__ == '__main__':
    backup(REGION)