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

    if status == 'FAILED':
        content = '![Failing]({0} "Failing") - See the [Logs]({1})'.format(badge, logs)
    else:
        content = '![Passing]({0} "Passing") - See the [Logs]({1})'.format(badge, logs)

    # SLACK_WEBHOOK = "https://hooks.slack.com/services/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"
    # r = requests.post(SLACK_WEBHOOK, json={"text": comment})

    return event
