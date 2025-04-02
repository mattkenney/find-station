#!/usr/bin/env python3

import boto3
from python_dynamodb_lock.python_dynamodb_lock import DynamoDBLockClient

client = boto3.client('dynamodb')
DynamoDBLockClient.create_dynamodb_table(client)
