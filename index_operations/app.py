import json

from registration import register_user


def lambda_handler(event, context):
    print(event)
    body = json.loads(event['body'])
    if body['action'] == 'register':
        return register_user(body)
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


