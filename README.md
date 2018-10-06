# gcp_dataproc
This repository consists various pythons scripts used to dynamically create a google data-proc cluster, launch an spark jobs on it and destroy the cluster once the job is completed. Ultimately saves lot of resources and money

# -----------------------------------------------
# Pre-requisites
# -----------------------------------------------
1. Create GCP account and enable the billing 
2. Enable the dataproc API

# -----------------------------------------------
# i. Requirements.txt
# -----------------------------------------------
RUN CMD
=======
# c:\Python27>python -m pip install -r C:\Users\Ravi\PycharmProjects\gcloud\learning\python_api_dataproc\conf\requirements.txt
# library contains the core Python library for accessing Google APIs, and also contains the OAuth 2.0 client library
google-api-python-client

To interact with Cloud Storage, you should install the gcloud-python library
============================================================================
google-cloud

This library provides an httplib2 transport for google-auth
=============================================================
google-auth-httplib2

# -------------------------------------------------
# ii. Steps to Run the scripts 
# -------------------------------------------------
To cluster
==========
C:\Python27\python.exe C:/Users/Ravi/PycharmProjects/gcloud/learning/python_api_dataproc/code/create_cluster.py --project_id learndataproc15days --zone asia-south1-c --cluster_name learndataproc-cluster1 --create_new_cluster True
To List clusters
================
C:\Python27\python.exe C:/Users/Ravi/PycharmProjects/gcloud/learning/python_api_dataproc/code/list_clusters.py --region asia-south1 learndataproc15days
To Launch spark job
====================
Befor running please update the jobId with unique value in the script. dont use previous job ids.
"reference": {
              "jobId": "firstsparkjobongcc0011"
            }
C:\Python27\python.exe C:/Users/Ravi/PycharmProjects/gcloud/learning/python_api_dataproc/code/submit_job.py --project_id learndataproc15days --zone asia-south1-c --cluster_name learndataproc-cluster1 --bucket_name dataproc-2768889b-97ca-4df4-9bf0-e9d9002f11fc-asia-south1 --job_file E:\Projects\Sample\HelloGCC\target\HelloGCC-1.0-SNAPSHOT.jar --main_class com.rab.dataproc.HelloSparkScala --job_type scala_spark
To Delete the Cluster
=====================
C:\Python27\python.exe C:/Users/Ravi/PycharmProjects/gcloud/learning/python_api_dataproc/code/del_cluster.py --project_id learndataproc15days --zone asia-south1-c --cluster_name learndataproc-cluster1 --del_cluster_flag True

# -------------------------------------------------
# iii. CMDS TO CONFIGURE GOOGLE CLOUD 
# -------------------------------------------------
# Prerequisite - install Google cloud SDK

CMDS TO CREATE GOOGLE STORAGE BUCKETS
=====================================
c:\Program Files (x86)\Google\Cloud SDK>gsutil mb gs://learndataproc15days_bucket
Creating gs://learndataproc15days_bucket/...
CMD TO SHOW ACTIVE CONFIG OF GOOGLE CLOUD
=========================================
c:\Program Files (x86)\Google\Cloud SDK>gcloud config list
[compute]
region = asia-south1
zone = asia-south1-c
[core]
account = uuuuuuu.lllll@gmail.com
disable_usage_reporting = True
project = learndataproc15days

Your active configuration is: [default]

c:\Program Files (x86)\Google\Cloud SDK>gcloud config list project
[core]
project = learndataproc15days

Your active configuration is: [default]

SET THE BUCKET'S DEFAULT ACL TO PUBLIC-READ, WHICH ENABLES USERS TO SEE THEIR UPLOADED IMAGES
==============================================================================================
c:\Program Files (x86)\Google\Cloud SDK>gsutil defacl set public-read gs://learn
dataproc15days_bucket
Setting default object ACL on gs://learndataproc15days_bucket/...
/ [1 objects]

TO SEE DISK USAGE OF BUCKET
============================
c:\Program Files (x86)\Google\Cloud SDK>gsutil du -s gs://learndataproc15days_bu
cket
0           gs://learndataproc15days_bucket

GCLOUD COMMAND-LINE TOOL CREDENTIALS (WHICH ARE AUTOMATICALLY CREATED ON APP ENGINE OR COMPUTE ENGINE)
======================================================================================================
gcloud auth application-default login
