import argparse
import googleapiclient.discovery


def get_region_from_zone(zone):
    try:
        region_as_list = zone.split('-')[:-1]
        return '-'.join(region_as_list)
    except (AttributeError, IndexError, ValueError):
        raise ValueError('Invalid zone provided, please check your input.')


# [START create_cluster]
def create_cluster(dataproc, project, zone, region, cluster_name):
    print('Creating cluster...')
    zone_uri = \
        'https://www.googleapis.com/compute/v1/projects/{}/zones/{}'.format(
            project, zone)
    cluster_data = {
        'projectId': project,
        'clusterName': cluster_name,
        'config': {
            'gceClusterConfig': {
                'zoneUri': zone_uri
            },
            'masterConfig': {
                'numInstances': 1,
                'machineTypeUri': 'n1-standard-1'
            },
            'workerConfig': {
                'numInstances': 2,
                'machineTypeUri': 'n1-standard-1'
            }
        }
    }
    result = dataproc.projects().regions().clusters().create(
        projectId=project,
        region=region,
        body=cluster_data).execute()
    return result


# [END create_cluster]


def wait_for_cluster_creation(dataproc, project_id, region, cluster_name):
    print('Waiting for cluster creation...')

    while True:
        result = dataproc.projects().regions().clusters().list(
            projectId=project_id,
            region=region).execute()
        cluster_list = result['clusters']
        cluster = [c
                   for c in cluster_list
                   if c['clusterName'] == cluster_name][0]
        if cluster['status']['state'] == 'ERROR':
            raise Exception(result['status']['details'])
        if cluster['status']['state'] == 'RUNNING':
            print("Cluster created.")
            break


# [START list_clusters_with_detail]
def list_clusters_with_details(dataproc, project, region):
    result = dataproc.projects().regions().clusters().list(
        projectId=project,
        region=region).execute()
    cluster_list = result['clusters']
    for cluster in cluster_list:
        print("{} - {}"
              .format(cluster['clusterName'], cluster['status']['state']))
    return result


# [END list_clusters_with_detail]


def get_cluster_id_by_name(cluster_list, cluster_name):
    """Helper function to retrieve the ID and output bucket of a cluster by
    name."""
    cluster = [c for c in cluster_list if c['clusterName'] == cluster_name][0]
    return cluster['clusterUuid'], cluster['config']['configBucket']


# [START get_client]
def get_client():
    """Builds an http client authenticated with the service account
    credentials."""
    dataproc = googleapiclient.discovery.build('dataproc', 'v1')
    return dataproc


# [END get_client]


def main(project_id, zone, cluster_name, create_new_cluster='False'):
    dataproc = get_client()
    region = get_region_from_zone(zone)
    try:
        if create_new_cluster == 'True':
            create_cluster(
                dataproc, project_id, zone, region, cluster_name)
            wait_for_cluster_creation(
                dataproc, project_id, region, cluster_name)

        cluster_list = list_clusters_with_details(
            dataproc, project_id, region)['clusters']

        (cluster_id, output_bucket) = (
            get_cluster_id_by_name(cluster_list, cluster_name))

        print("Cluster_id" + cluster_id + "Bucket Info" + output_bucket)

    finally:
        if create_new_cluster == 'True':
            print("Cluster Created Successfully, Now you can use/del the cluster")
        else:
            print("Cluster already Exists, Now you can use/del the cluster")



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
        '--create_new_cluster',
        help='States if the cluster should be created', required=True)

    args = parser.parse_args()
    main(
        args.project_id, args.zone, args.cluster_name, args.create_new_cluster)
