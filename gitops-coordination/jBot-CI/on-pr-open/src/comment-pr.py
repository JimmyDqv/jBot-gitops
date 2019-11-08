import json
import logging
import boto3
import os

log = logging.getLogger('jBot')
log.setLevel(logging.DEBUG)


def handler(event, context):
    log.debug(json.dumps(event, indent=2))

    comment = 'Build with id {} has started....'.format(event['buildId'])
    log.debug(comment)

    client = boto3.client('codecommit')
    client.post_comment_for_pull_request(
        pullRequestId=event['pullRequestId'],
        repositoryName=event['repositoryNames'][0],
        beforeCommitId=event['destinationCommit'],
        afterCommitId=event['sourceCommit'],
        content=comment,
        clientRequestToken=event['buildId']
    )

    return event
