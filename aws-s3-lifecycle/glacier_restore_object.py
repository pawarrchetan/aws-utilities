import logging
import boto3
from botocore.exceptions import ClientError


def restore_object(bucket_name, object_name, days, retrieval_type='Standard'):
    """Restore an archived S3 Glacier object in an Amazon S3 bucket

    :param bucket_name: string
    :param object_name: string
    :param days: number of days to retain restored object
    :param retrieval_type: 'Standard' | 'Expedited' | 'Bulk'
    :return: True if a request to restore archived object was submitted, otherwise
    False
    """

    # Create request to restore object
    request = {'Days': days,
               'GlacierJobParameters': {'Tier': retrieval_type}}

    # Submit the request
    s3 = boto3.client('s3')
    try:
        s3.restore_object(Bucket=bucket_name, Key=object_name, RestoreRequest=request)
    except ClientError as e:
        # NoSuchBucket, NoSuchKey, or InvalidObjectState error == the object's
        # storage class was not GLACIER
        logging.error(e)
        return False
    return True


def main():
    """Exercise restore_object()"""

    # Assign these values before running the program
    test_bucket_name = 'BUCKET_NAME'
    test_object_name = 'OBJECT_NAME'

    # Set up logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    # Restore archived object for two days. Expedite the restoration.
    success = restore_object(test_bucket_name, test_object_name, 2, 'Expedited')
    if success:
        logging.info(f'Submitted request to restore {test_object_name} '
                     f'in {test_bucket_name}')


if __name__ == '__main__':
    main()