# ami_cleanup.py

from datetime import datetime
import aws_utils as awsutils
import os

REGION = os.environ['AWS_REGION']

def cleanup(region_id=REGION):
    '''This method searches for all AMI images with a tag of RemoveOn
       and a value of YYYYMMDD of the day its ran on then removes it
    '''
    today = datetime.utcnow().strftime('%Y%m%d')
    session = awsutils.get_session(region_id)
    client = session.client('ec2')
    resource = session.resource('ec2')
    images = client.describe_images(Filters=[{'Name': 'tag:RemoveOn', 'Values': [today]}])
    for image_data in images['Images']:
        image = resource.Image(image_data['ImageId'])
        name_tag = [tag['Value'] for tag in image.tags if tag['Key'] == 'Name']
        if name_tag:
            print(f"Deregistering {name_tag[0]}")
        image.deregister()

if __name__ == '__main__':
    cleanup(REGION)