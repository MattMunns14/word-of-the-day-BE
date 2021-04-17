import boto3
import json
import os
from utils import dict_to_dynamo_json, dynamo_item_to_dict
import hashlib


HEADERS = {
            'Access-Control-Allow-Headers': "*",
            'Access-Control-Allow-Origin': 'https://wordsoftheday.org',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        }


def register_user(registration_payload: dict):
    email = registration_payload['email']
    dynamo = boto3.client('dynamodb')
    if user_exists(email, dynamo):
        return {
            'headers': HEADERS,
            "statusCode": 400,
            "body": json.dumps({
                "message": "Email address is already registered",
            }),
        }
    else:
        user_item = {
            'user_email': email,
            'password': hashlib.md5(registration_payload['password'].encode('utf-8')).hexdigest()
        }
        dynamo.put_item(
            TableName=os.environ['USERS_TABLE'],
            Item=dict_to_dynamo_json(user_item)
        )
        return {
            'headers': HEADERS,
            'statusCode': 200,
            "body": json.dumps({
                "message": "Registration successful"
            })

        }


def user_exists(email, dynamo):

    email_item = dynamo.get_item(TableName=os.environ['USERS_TABLE'],
                                 Key={'user_email': {'S': email}})
    try:
        job_item = dynamo_item_to_dict(email_item['Item'])
        return True
    except KeyError:
        return False





