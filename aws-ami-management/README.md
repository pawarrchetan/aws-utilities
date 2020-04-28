# AWS AMI Automated Creation & Deletion System
A simple AWS python project to help automate creation and deletion of AMIs. The scripts are written in Python.
The scripts can be easily used for serveless platform.

## Motivation
Creating an AMI automatically snapshots all the associated EBS volumes for that instance. This makes instance recovery much more reliable and faster. A daily or weekly backup schedule is recommended for instances and to make sure you have a backup if ever needed. An additional script also removes the automatically created AMIs and any associated snapshots as per the settings.

## Setup / Installation of the script

1. Setup Python3 virtual Environment
```
$ python -m venv venv
$ source venv/bin/activate
(venv)$ pip install boto3 awscli
```

2. Configure the credentials for the boto3 library using the awscli library making sure to add in the credentials for the Access Key and Secret Key.
```
$ aws configure
AWS Access Key ID [****************3XRQ]: **************
AWS Secret Access Key [****************UKjF]: ****************
Default region name [None]:
Default output format [None]:
```

3. Make sure if you have the right Tag "BackUp" to the EC2 instance that you need to create the AMI for.

4. Executing script to Create AMI using Tags.
```
$ python3.7 ami_creation.py                                                                                                              [9:49:06]
Creating Backup: Sample_InstanceId(i-0b40xxxxxxxx4223c5)_CreatedOn(20200409)
```

5. The ami_cleanup.py script looks for tag "RemoveOn" which is created by Step 4 and can be run as a cron to schedule daily cleanup of old images.
```
$ python3.7 ami_cleanup.py                                                                                                              [9:49:06]
Deregistering Sample_InstanceId(i-0b40xxxxxxxx4223c5)_CreatedOn(20200409)

```
## Lambda Function
The file `handler.py` can be used to create a serverless function to do the backup and cleanup for the AMIs automatically on a schedulec cron job.

## Setting the tags for EC2 instances  

Set the tags on the instances you want backed up.  
* **BackUp**: True 


## Notes

- This is another open source project bought to you by [https://github.com/pawarrchetan).
- Please submit your pull requests or suggestions to improve this script.