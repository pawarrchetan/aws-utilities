# What is S3

---

S3 stands for **S**imple **S**torage **S**ervice. An Amazon service which was released on

The one word answer for it's widely used popularity is the ease of use at any scale ranging from 1 byte to peta bytes.

S3 is used to store your data on internet. In layman terms

* Imagine  a Folder in your C drive. Just that the Folder is present on internet.
* Imagine a Directory on your UNIX/UBUNTU server, just that the directory is on internet.

  ?![](/assets/s31.jpg)

* You can store your personal files \( Photos, videos, documents \).

* Database administrators can use it to store the RMAN Backups

* Do you have a website, then you can store your static pages like Images, Java Script, HTML,CSS.

# S3 buckets

---

Amazon Bucket is a container of data. In technical terms “A bucket is a Container with objects Inside”.

A few things to keep in mind when working with AWS S3 buckets,

* Buckets names are unique
* Buckets are regional
* By default you can create 101 buckets in an AWS account, you can always work with AWS support and increase the limit.

#### Find out all the S3 buckets in your AWS Account.

By default you can only create 101 S3 buckets in an AWS account. If needed you can work with AWS to increase the limit,

Here is a quick script to list all the S3 buckets in your account

* The script `list_buckets.py` can be used to list all the buckets in the AWS account.

#### LifeCycle

##### Create LifeCycle

* The script `put_bucket_lifecycle_configuration.py` can be used to list all the buckets in the AWS account and then apply the policy mentioned in the script.
