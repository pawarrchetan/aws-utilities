import boto3
import sys
import datetime
 
def get_cpu_util(instanceID,startTime,endTime):

    client = boto3.client('cloudwatch')
    response = client.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[
                {
                'Name': 'InstanceId',
                'Value': instanceID
                },
            ],
             
            StartTime=startTime,
            EndTime=endTime,
            Period=3600,
            Statistics=[
                'Average',
            ],
            Unit='Percent'
        )
    for k, v in response.items():
        if k == 'Datapoints':
            for y in v:
                return "{0:.2f}".format(y['Average'])

# get all instances
instanceIDs=[]
ec2 = boto3.resource('ec2')
instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
now = datetime.datetime.now()
now_minus_5 = datetime.datetime.now() - datetime.timedelta(minutes=240)
for instance in instances:
    tmpDict=get_cpu_util(instance.id, now_minus_5, now)
    print (f"instance-id : {instance.id} CPUUtilization : {tmpDict}")
    # if tmpDict:
    #     for tags in instance.tags:
    #         try:
    #             if tags['Key'] == 'Name':
    #               tmpDict['Name']=tags['Value']
    #               break
    #         except KeyError: pass
    #     else:
    #         print("Name not found")

def lambda_handler(event, context):
    instance_id = event['detail']['instance-id']
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(instance_id)
    now = datetime.datetime.now()
    now_minus_5 = now - datetime.timedelta(minutes = 5)
    cpustatus = get_cpu_util(instance.id, now_minus_5, now)