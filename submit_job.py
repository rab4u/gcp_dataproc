import argparse
import os

from google.cloud import storage
import googleapiclient.discovery


def get_job_file(filename):
    f = open(filename, 'rb')
    return f, os.path.basename(filename)


def upload_job_file(project_id, bucket_name, filename, file):
    print('Uploading job file to GCS')
    client = storage.Client(project=project_id)
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(filename)
    blob.upload_from_file(file)
    print('Uploading completed successfully')


def download_output(project_id, cluster_id, output_bucket, job_id):
    print('Downloading output file')
    client = storage.Client(project=project_id)
    bucket = client.get_bucket(output_bucket)
    output_blob = (
        'google-cloud-dataproc-metainfo/{}/jobs/{}/{}/driveroutput.000000000'
        .format(cluster_id, job_id, 'attempt_1'))
    return bucket.blob(output_blob).download_as_string()


def submit_sacla_spark_job(dataproc, project, region,
                       cluster_name, bucket_name, filename, main_class):
    """Submits the Pyspark job to the cluster, assuming `filename` has
    already been uploaded to `bucket_name`"""
    job_details = {
          "projectId": project,
          "job": {
            "placement": {
              "clusterName": cluster_name
            },
            "reference": {
              "jobId": "firstsparkjobongcc0010"
            },
            "sparkJob": {
              "args": [],
              "mainClass": main_class,
              "jarFileUris": [
                'gs://{}/{}'.format(bucket_name, filename)
              ]
            },
            "scheduling": {
              "maxFailuresPerHour": 5
            }
          }
        }
    result = dataproc.projects().regions().jobs().submit(
        projectId=project,
        region=region,
        body=job_details).execute()
    job_id = result['reference']['jobId']
    print('Submitted job ID {}'.format(job_id))
    return job_id


def wait_for_job(dataproc, project, region, job_id):
    print('Waiting for job to finish...')
    while True:
        result = dataproc.projects().regions().jobs().get(
            projectId=project,
            region=region,
            jobId=job_id).execute()
        # Handle exceptions
        if result['status']['state'] == 'ERROR':
            raise Exception(result['status']['details'])
        elif result['status']['state'] == 'DONE':
            print('Job finished.')
            return result


def get_region_from_zone(zone):
    try:
        region_as_list = zone.split('-')[:-1]
        return '-'.join(region_as_list)
    except (AttributeError, IndexError, ValueError):
        raise ValueError('Invalid zone provided, please check your input.')


def get_client():
    """Builds an http client authenticated with the service account
    credentials."""
    dataproc = googleapiclient.discovery.build('dataproc', 'v1')
    return dataproc


def list_clusters_with_details(dataproc, project, region):
    result = dataproc.projects().regions().clusters().list(
        projectId=project,
        region=region).execute()
    cluster_list = result['clusters']
    for cluster in cluster_list:
        print("{} - {}"
              .format(cluster['clusterName'], cluster['status']['state']))
    return result


def get_cluster_id_by_name(cluster_list, cluster_name):
    """Helper function to retrieve the ID and output bucket of a cluster by
    name."""
    cluster = [c for c in cluster_list if c['clusterName'] == cluster_name][0]
    print(cluster)
    return cluster['clusterUuid'], cluster['config']['configBucket']


def main(project_id, zone, cluster_name, bucket_name, job_file, main_class, job_type='scala_spark'):
    dataproc = get_client()
    region = get_region_from_zone(zone)
    try:
        spark_file, spark_filename = get_job_file(job_file)
        upload_job_file(project_id, bucket_name, spark_filename, spark_file)

        cluster_list = list_clusters_with_details(dataproc, project_id, region)['clusters']

        (cluster_id, output_bucket) = (get_cluster_id_by_name(cluster_list, cluster_name))

        if job_type == 'scala_spark':
            job_id = submit_sacla_spark_job(dataproc, project_id, region, cluster_name, bucket_name, spark_filename,
                                            main_class)
            wait_for_job(dataproc, project_id, region, job_id)

        output = download_output(project_id, cluster_id, output_bucket, job_id)
        print('Received job output {}'.format(output))
    finally:
        spark_file.close()
        print("***********END*************")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--project_id', help='Project ID you want to access.', required=True),
    parser.add_argument(
        '--zone', help='Zone to create clusters in/connect to', required=True)
    parser.add_argument(
        '--cluster_name',
        help='Name of the cluster to create/connect to', required=True)
    parser.add_argument(
        '--bucket_name',
        help='Name of the google cloud bucket', required=True)
    parser.add_argument(
        '--job_file',
        help='Job file path', required=True)
    parser.add_argument(
        '--main_class',
        help='Main class of job', required=True)
    parser.add_argument(
        '--job_type',
        help='Type of job (example : scala_spark,pi_spark,map_reduce)', required=True)

    args = parser.parse_args()
    main(
        args.project_id, args.zone, args.cluster_name, args.bucket_name, args.job_file, args.main_class, args.job_type)

