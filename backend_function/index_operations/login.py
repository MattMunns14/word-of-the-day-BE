import hashlib
import json
import os
import time

import boto3
import jwt

from .utils import dynamo_item_to_dict, user_exists

HEADERS = {
            'Access-Control-Allow-Headers': "*",
            'Access-Control-Allow-Origin': 'https://wordsoftheday.org',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        }


def verify_token(body: dict):
    token = body['token_to_verify']
    try:
        user_jwt = jwt.decode(token, key=os.environ['SECRET'], algorithms=['HS256'])
    except jwt.exceptions.InvalidSignatureError:
        return {
            'headers': HEADERS,
            'statusCode': 400,
            "body": json.dumps({'message': 'Nice try Bozo'})
        }
    return {
        'headers': HEADERS,
        'statusCode': 200,
        'body': json.dumps({'message': 'Valid Token'})
    }


def login_user_and_return_token(body: dict):
    required_keys = ['email', 'password']
    for key in required_keys:
        if key not in body:
            return {
                'headers': HEADERS,
                "statusCode": 400,
                "body": json.dumps({
                    "message": f"Request is missing key {key}.",
                }),
            }

    dynamo = boto3.client('dynamodb')
    email = body['email']
    password = body['password']

    if not user_exists(email, dynamo):
        return {
            'headers': HEADERS,
            "statusCode": 400,
            "body": json.dumps({
                "message": "User does not exist",
            }),
        }

    email_item = dynamo.get_item(TableName=os.environ['USERS_TABLE'],
                                 Key={'user_email': {'S': email}})
    user_password = dynamo_item_to_dict(email_item['Item'])['password']

    hashed_input_password = hashlib.md5(password.encode('utf-8')).hexdigest()

    if user_password == hashed_input_password:
        user_jwt = jwt.encode({'user_email': email, 'timestamp': time.time()},
                              os.environ['SECRET'],
                              algorithm='HS256')

        return {
            'headers': HEADERS,
            'statusCode': 200,
            'body': json.dumps(
                {
                    'token': user_jwt
                }
            )
        }
    else:
        return {
            'headers': HEADERS,
            "statusCode": 400,
            "body": json.dumps({
                "message": "Incorrect password",
            }),
        }



