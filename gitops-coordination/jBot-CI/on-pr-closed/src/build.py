import json
import logging
import boto3
import os

log = logging.getLogger('jBot')
log.setLevel(logging.DEBUG)


def handler(event, context):
    log.debug(json.dumps(event, indent=2))

    sourceVersion = event['REPO_REF_FULL_NAME'] + \
        '^{'+event['COMMIT_ID']+'}'
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
                'value': event['COMMIT_ID'],
                'type': 'PLAINTEXT'
            },
            {
                'name': 'REPO_REF_FULL_NAME',
                'value': event['REPO_REF_FULL_NAME'],
                'type': 'PLAINTEXT'
            },
            {
                'name': 'REPO_NAME',
                'value': event['REPO_NAME'],
                'type': 'PLAINTEXT'
            },
            {
                'name': 'CALLER_ARN',
                'value': event['CALLER_ARN'],
                'type': 'PLAINTEXT'
            }
        ]
    )

    buildId = response['build']['id']
    comment = 'Build with id {} has started....'.format(buildId)
    log.debug(comment)

    return event
