import json
import logging
import boto3
import os

import uuid

log = logging.getLogger('jBot')
log.setLevel(logging.DEBUG)


def handler(event, context):
    log.debug(json.dumps(event, indent=2))

    codebuildProject = os.environ['CODE_BUILD_PROJECT']
    environment = os.environ['ENV_ALIAS']
    artifactLocation = "{0}/{1}".format(event['bucket']
                                        ['name'], event['object']['key'])

    client = boto3.client('codebuild')
    response = client.start_build(
        projectName=codebuildProject,
        sourceTypeOverride='S3',
        sourceLocationOverride=artifactLocation,
        environmentVariablesOverride=[
            {
                'name': 'ENV_ALIAS',
                'value': environment,
                'type': 'PLAINTEXT'
            }
        ]
    )

    return event
