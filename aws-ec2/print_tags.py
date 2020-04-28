import boto3
import json

client = boto3.client("ec2")
resource = boto3.resource("ec2")

response = client.describe_instances(
    Filters=[
        {
            'Name': 'tag:Name',
            'Values': [
                'myapp-*'
            ]
        },
        {
            'Name': 'instance-state-name',
            'Values': [
                'running',
            ]
        }
    ]
)['Reservations']

instanceList = []
for reservation in response:
    ec2_instances = reservation["Instances"]
    for instance in ec2_instances:
        InstanceId = (instance['InstanceId'])
        #InstanceState = (instance['State']['Name'])
        #InstanceLaunchTime = (instance['LaunchTime'])

        ec2instance = resource.Instance(InstanceId)
        InstanceName = []
        for tags in ec2instance.tags:
            if tags["Key"] == 'Name':
                InstanceName = tags['Value']

        fInstance = (InstanceName, InstanceId)
        InstanceDetails = (",".join(fInstance))
        instanceList.append(fInstance)

print(json.dumps(instanceList, indent=4))