import json
import logging
import boto3
import os
import uuid

log = logging.getLogger('jBot')
log.setLevel(logging.DEBUG)


def handler(event, context):
    log.debug(json.dumps(event, indent=2))

    envAlias = os.environ['ENVIRONMENT_ALIAS']
    artifactBucket = os.environ['S3_ARTIFACT_BUCKET']
    commitId = event['COMMIT_ID']
    repoName = event['REPO_NAME']
    repoRefFullName = event['REPO_REF_FULL_NAME']
    caller = event['CALLER']
    logs = event['LOGS_DEEP_LINK']
    status = event['STATUS']
    artifactLocation = event['ARTIFACT_LOCATION']

    sourceArtifactKey = artifactLocation.split(':')[-1]
    buildId = sourceArtifactKey.split('/')[-1]

    log.debug(sourceArtifactKey)

    destinationArtifactKey = '{0}/{1}/{2}/artifact.zip'.format(
        envAlias, commitId, buildId)

    client = boto3.client('s3')
    response = client.copy_object(
        Bucket=artifactBucket,
        Key=destinationArtifactKey,
        CopySource='{}/artifact.zip'.format(sourceArtifactKey)
    )

    return event
