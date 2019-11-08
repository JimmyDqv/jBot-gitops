import json
import logging
import boto3
import os
import uuid

log = logging.getLogger('jBot')
log.setLevel(logging.DEBUG)


def handler(event, context):
    log.debug(json.dumps(event, indent=2))

    pullRequestId = event['PR_ID']
    repoName = event['REPO_NAME']
    destCommitId = event['DEST_COMMIT_ID']
    commitId = event['COMMIT_ID']
    status = event['STATUS']
    logs = event['LOGS_DEEP_LINK']
    badge = event['BADGE']
    environmentUrl = event['ENVIRONMENT_URL']

    if status == 'FAILED':
        content = '![Failing]({0} "Failing") - See: [Logs]({1})'.format(badge, logs)
    else:
        content = '![Passing]({0} "Passing") - See: [Logs]({1}) | [Test Environment]({2})'.format(
            badge, logs, environmentUrl)

    client = boto3.client('codecommit')
    client.post_comment_for_pull_request(
        pullRequestId=pullRequestId,
        repositoryName=repoName,
        beforeCommitId=destCommitId,
        afterCommitId=commitId,
        content=content,
        clientRequestToken=str(uuid.uuid1())
    )

    return event
