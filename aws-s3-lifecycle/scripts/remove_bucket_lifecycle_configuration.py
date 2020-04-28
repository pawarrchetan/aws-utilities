import logging
import boto3
from botocore.exceptions import ClientError

def remove_bucket_lifecycle_configuration(bucket_name):
    """Delete the lifecycle configuration of an Amazon S3 bucket

    :param bucket_name: string
    :return: True if lifecycle configuration was deleted, otherwise False
    """

    # Set the configuration
    s3 = boto3.client('s3')
    try:
        s3.BucketLifecycle(Bucket=bucket_name).delete()
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
    """Exercise remove_bucket_lifecycle_configuration()"""

    # Assign this value before running the program
    bucket_list = get_bucket_list()

    for bucket in bucket_list:
        test_bucket_name = bucket
        # Set up logging
        logging.basicConfig(level=logging.DEBUG,
                            format='%(levelname)s: %(asctime)s: %(message)s')
        # Set the bucket's lifecycle configuration
        success = remove_bucket_lifecycle_configuration(test_bucket_name)
        if success:
            logging.info(
                f'The lifecycle configuration was set for {test_bucket_name}')


if __name__ == '__main__':
    main()
