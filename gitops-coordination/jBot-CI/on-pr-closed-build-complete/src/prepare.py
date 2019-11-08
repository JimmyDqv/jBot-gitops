import json
import logging
import boto3
import os
import uuid

log = logging.getLogger('jBot')
log.setLevel(logging.DEBUG)


def handler(event, context):
    log.debug(json.dumps(event, indent=2))

    details = event['detail']

    # Read all the environment variables
    environmentVariables = details['additional-information']['environment']['environment-variables']

    commitId = get_value(environmentVariables, 'COMMIT_ID')
    repoName = get_value(environmentVariables, 'REPO_NAME')
    repoRefFullName = get_value(environmentVariables, 'REPO_REF_FULL_NAME')
    caller = get_value(environmentVariables, 'CALLER_ARN')

    logs = details['additional-information']['logs']['deep-link']
    status = details['build-status']

    artifactLocation = details['additional-information']['artifact']['location']

    return {
        "COMMIT_ID": commitId,
        "REPO_NAME": repoName,
        "REPO_REF_FULL_NAME": repoRefFullName,
        "CALLER": caller,
        "LOGS_DEEP_LINK": logs,
        "STATUS": status,
        "ARTIFACT_LOCATION": artifactLocation
    }


def get_value(list, key):
    for item in list:
        if item['name'] == key:
            return item['value']
