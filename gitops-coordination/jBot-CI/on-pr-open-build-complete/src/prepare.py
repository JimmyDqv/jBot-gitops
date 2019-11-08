import json
import logging
import boto3
import os
import uuid

log = logging.getLogger('jBot')
log.setLevel(logging.DEBUG)


def handler(event, context):
    log.debug(json.dumps(event, indent=2))

    # Due to bug in console we need to use the CodeBuild badge URL to have it rendering correctly.
    # We can't use the direct link to S3 based resources.
    # See: https://forums.aws.amazon.com/thread.jspa?threadID=273712

    region = event['region']
    if region != 'us-east-1':
        s3_prefix = 's3-{0}'.format(region)
    else:
        s3_prefix = 's3'
    badge_failing = 'https://{0}.amazonaws.com/codefactory-{1}-prod-default-build-badges/failing.svg'.format(
        s3_prefix, region)
    badge_success = 'https://{0}.amazonaws.com/codefactory-{1}-prod-default-build-badges/passing.svg'.format(
        s3_prefix, region)

    cfn_base_name = os.environ['CLOUDFORMATION_BASE_NAME']

    details = event['detail']

    # # Get the Badge URL from CodeBuild
    # client = boto3.client('codebuild')
    # response = client.batch_get_projects(
    #     names=[
    #         details['project-name'],
    #     ]
    # )
    # badge = response['projects'][0]['badge']['badgeRequestUrl']

    # Read all the environment variables
    environmentVariables = details['additional-information']['environment']['environment-variables']

    pullRequestId = get_value(environmentVariables, 'PR_ID')
    repoName = get_value(environmentVariables, 'REPO_NAME')
    destCommitId = get_value(environmentVariables, 'DEST_COMMIT_ID')
    commitId = get_value(environmentVariables, 'COMMIT_ID')

    logs = details['additional-information']['logs']['deep-link']
    status = details['build-status']
    if status == 'FAILED':
        badge = badge_failing
    else:
        badge = badge_success

    # Get the EnvironmentUrl from CloudFormation
    client = boto3.client('cloudformation')
    response = client.describe_stacks(
        StackName='{0}{1}'.format(cfn_base_name, pullRequestId)
    )

    environmentUrl = get_output_value(
        response['Stacks'][0]['Outputs'], 'EnvironmentUrl')

    return {
        "PR_ID": pullRequestId,
        "REPO_NAME": repoName,
        "DEST_COMMIT_ID": destCommitId,
        "COMMIT_ID": commitId,
        "BADGE": badge,
        "STATUS": status,
        "LOGS_DEEP_LINK": logs,
        "ENVIRONMENT_URL": environmentUrl,
    }


def get_value(list, key):
    for item in list:
        if item['name'] == key:
            return item['value']


def get_output_value(list, key):
    for item in list:
        if item['OutputKey'] == key:
            return item['OutputValue']
