import argparse
import googleapiclient.discovery


def get_region_from_zone(zone):
    try:
        region_as_list = zone.split('-')[:-1]
        return '-'.join(region_as_list)
    except (AttributeError, IndexError, ValueError):
        raise ValueError('Invalid zone provided, please check your input.')


# [START get_client]
def get_client():
    """Builds an http client authenticated with the service account
    credentials."""
    dataproc = googleapiclient.discovery.build('dataproc', 'v1')
    return dataproc


# [START delete]
def delete_cluster(dataproc, project, region, cluster):
    print('Tearing down cluster')
    result = dataproc.projects().regions().clusters().delete(
        projectId=project,
        region=region,
        clusterName=cluster).execute()
    return result
# [END delete]


def main(project_id, zone, cluster_name, del_cluster_flag='False'):
    dataproc = get_client()
    region = get_region_from_zone(zone)
    try:
        if del_cluster_flag == 'True':
            delete_cluster(dataproc, project_id, region, cluster_name)

    finally:
        if del_cluster_flag == 'True':
            print("Cluster Deleted Successfully...")
        else:
            print("Sorry Cannot Delete the Cluster, Please check the settings")



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
        '--del_cluster_flag',
        help='States if the cluster should be created', required=True)

    args = parser.parse_args()
    main(args.project_id, args.zone, args.cluster_name, args.del_cluster_flag)
