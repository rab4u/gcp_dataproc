import argparse

import googleapiclient.discovery


# [START list_clusters]
def list_clusters(dataproc, project, region):
    result = dataproc.projects().regions().clusters().list(
        projectId=project,
        region=region).execute()
    return result
# [END list_clusters]


# [START get_client]
def get_client():
    """Builds a client to the dataproc API."""
    dataproc = googleapiclient.discovery.build('dataproc', 'v1')
    return dataproc
# [END get_client]


def main(project_id, region):
    dataproc = get_client()
    result = list_clusters(dataproc, project_id, region)
    print(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'project_id', help='Project ID you want to access.'),
    # Sets the region to "global" if it's not provided
    # Note: sub-regions (e.g.: us-central1-a/b) are currently not supported
    parser.add_argument(
        '--region', default='global', help='Region to create clusters in')

    args = parser.parse_args()
    main(args.project_id, args.region)