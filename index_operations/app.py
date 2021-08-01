import json

from registration import register_user
from login import login_user_and_return_token, verify_token


def lambda_handler(event, context):
    print(event)
    body = json.loads(event['body'])
    if body['action'] == 'register':
        return register_user(body)
    elif body['action'] == 'login':
        return login_user_and_return_token(body)
    elif body['action'] == 'verify_token':
        return verify_token(body)
    else:
        return {
            'headers': {
                'Access-Control-Allow-Headers': "*",
                'Access-Control-Allow-Origin': 'https://wordsoftheday.org',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            "statusCode": 400,
            "body": json.dumps({
                "message": "Action is not supported",
            }),
        }


