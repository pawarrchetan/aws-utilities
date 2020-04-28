#!/bin/sh

for bucket in `aws s3 ls --human-readable | awk -F ' ' '{print $3}' | egrep -v "avid-cloudtrail|log|glue|athena|config|elastic|kops|account|customer-message|email|terraform|cf|assets-epilot|frontend|catchall|internal"`
do 
    for folder in `aws s3 ls s3://$bucket --human-readable | awk -F ' ' '{print $2}'`
    do
        aws s3api list-objects-v2 --bucket $bucket --prefix $folder --query "Contents[?StorageClass=='GLACIER']" --output text | awk -F ' ' '{print $2}' >> objects-$bucket.txt
    done

    for object in `cat objects-$bucket.txt`
    do
        echo "Begin restoring $object"
        aws s3api restore-object --restore-request Days=365,GlacierJobParameters={Tier=Standard} --bucket $bucket --key "$object"
        echo "Done restoring $object"
    done
done