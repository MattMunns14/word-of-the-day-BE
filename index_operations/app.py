import json

from registration import register_user


def lambda_handler(event, context):
    print(event)
    if event['body']['action'] == 'register':
        return register_user(event['body'])
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


