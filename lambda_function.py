"""
AWS Lambda handler function for the find-station feature.
"""

import json
import logging

import boto3
from python_dynamodb_lock.python_dynamodb_lock import DynamoDBLockClient

from request_handler import find_closest_station

logger = logging.getLogger()

# use distributed locking with lock in AWS DynamoDB
dynamodb_resource = boto3.resource('dynamodb')
lock_client = DynamoDBLockClient(dynamodb_resource)


def lambda_handler(event, context):
    """AWS Lambda Function handler"""
    logging.info(
        "lambda_handler event",
        extra={"context": str(context), "event": event},
    )
    # AWS API Gateway uses the first path segment as its "Stage"
    # and strips it off, we add back "/api" as a virtual first segment
    # so that the path is the same when running in AWS as in local development
    path = '/api' + event['path']

    # demontrate distributed locking
    # use `path` as lock key so only one search of the same location can
    # execute at one time
    with lock_client.acquire_lock(path):
        payload = find_closest_station(event['httpMethod'], path)

    # return the format expected by AWS API Gateway
    return {
        'statusCode': payload.get('statusCode', 200),
        'body': json.dumps(payload),
    }
