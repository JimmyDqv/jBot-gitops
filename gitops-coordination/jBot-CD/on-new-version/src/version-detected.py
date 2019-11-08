import json
import logging
import boto3
import os

import uuid

log = logging.getLogger('jBot')
log.setLevel(logging.DEBUG)


def handler(event, context):
    log.debug(json.dumps(event, indent=2))

    stateMachine = os.environ['STATE_MACHINE']
    log.debug(stateMachine)

    inputData = event['Records'][0]['s3']
    print("inputdata")
    log.debug(json.dumps(inputData, indent=2))
    print("inputdata")
    json.dumps(inputData)

    client = boto3.client('stepfunctions')
    response = client.start_execution(
        stateMachineArn=stateMachine,
        name=str(uuid.uuid4()),
        input=json.dumps(inputData)
    )

    return response['ResponseMetadata']
