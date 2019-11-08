import json
import logging
import boto3
import os

log = logging.getLogger('jBot')
log.setLevel(logging.DEBUG)


def handler(event, context):
    log.debug(json.dumps(event, indent=2))

    prDetails = event['detail']

    sourceVersion = prDetails['sourceReference'] + \
        '^{'+prDetails['sourceCommit']+'}'
    log.debug(sourceVersion)

    codebuild_project = os.environ['CODE_BUILD_PROJECT']
    log.debug(codebuild_project)

    client = boto3.client('codebuild')
    response = client.start_build(
        projectName=codebuild_project,
        sourceVersion=sourceVersion,
        environmentVariablesOverride=[
            {
                'name': 'COMMIT_ID',
                'value': prDetails['sourceCommit'],
                'type': 'PLAINTEXT'
            },
            {
                'name': 'ENV_ALIAS',
                'value': prDetails['pullRequestId'],
                'type': 'PLAINTEXT'
            },
            {
                'name': 'PR_ID',
                'value': prDetails['pullRequestId'],
                'type': 'PLAINTEXT'
            },
            {
                'name': 'REPO_NAME',
                'value': prDetails['repositoryNames'][0],
                'type': 'PLAINTEXT'
            },
            {
                'name': 'DEST_COMMIT_ID',
                'value': prDetails['destinationCommit'],
                'type': 'PLAINTEXT'
            }
        ]
    )

    buildId = response['build']['id']
    comment = 'Build with id {} has started....'.format(buildId)
    log.debug(comment)

    prDetails['buildId'] = buildId

    return prDetails
