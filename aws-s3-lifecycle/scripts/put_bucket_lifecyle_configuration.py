import logging
import boto3
from botocore.exceptions import ClientError

# Lifecycle configuration settings
lifecycle_config_settings = {
    'Rules': [
        {
            'Expiration': {'Days': 365},
            'ID': 'Current-Version-Rule',
            'Filter': {'Prefix': ''},
            'Status': 'Enabled',
            'Transitions': [{'Days': 90, 'StorageClass': 'GLACIER'}],
            'AbortIncompleteMultipartUpload': {'DaysAfterInitiation': 7}
        },
        {
            'Expiration': {'ExpiredObjectDeleteMarker': True},
            'ID': 'Previous-Version-Rule',
            'Filter': {'Prefix': ''},
            'Status': 'Enabled',
            'NoncurrentVersionTransitions': [{'NoncurrentDays': 30, 'StorageClass': 'GLACIER'}],
            'NoncurrentVersionExpiration': {'NoncurrentDays': 365},
            'AbortIncompleteMultipartUpload': {'DaysAfterInitiation': 7}
        }
    ]
}


def put_bucket_lifecycle_configuration(bucket_name, lifecycle_config):
    """Set the lifecycle configuration of an Amazon S3 bucket

    :param bucket_name: string
    :param lifecycle_config: dict of lifecycle configuration settings
    :return: True if lifecycle configuration was set, otherwise False
    """

    # Set the configuration
    s3 = boto3.client('s3')
    try:
        s3.put_bucket_lifecycle_configuration(Bucket=bucket_name,
                                              LifecycleConfiguration=lifecycle_config)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def get_bucket_list():
    """Get the list of buckets in the account"""
    # Create an S3 client
    s3 = boto3.client('s3')
    # Call S3 to list current buckets
    response = s3.list_buckets()
    # Get a list of all bucket names from the response
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    # # Print out the bucket list
    # print("Bucket List: %s" % buckets)
    return buckets


def main():
    """Exercise get_bucket_list()"""
    """Exercise put_bucket_lifecycle_configuration()"""

    # Assign this value before running the program
    bucket_list = get_bucket_list()

    for bucket in bucket_list:
        test_bucket_name = bucket
        # Set up logging
        logging.basicConfig(level=logging.DEBUG,
                            format='%(levelname)s: %(asctime)s: %(message)s')
        # Set the bucket's lifecycle configuration
        success = put_bucket_lifecycle_configuration(test_bucket_name,
                                                     lifecycle_config_settings)
        if success:
            logging.info(
                f'The lifecycle configuration was set for {test_bucket_name}')


if __name__ == '__main__':
    main()
