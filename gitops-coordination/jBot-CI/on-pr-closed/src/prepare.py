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

    return {
        "COMMIT_ID": details['sourceCommit'],
        "REPO_REF_FULL_NAME": details['destinationReference'],
        "REPO_NAME": details['repositoryNames'][0],
        "CALLER_ARN": details['callerUserArn'],
        "AUTHOR": details['author'],
        "IS_MERGED": details['isMerged'],
        "PR_ID": details['pullRequestId']
    }
