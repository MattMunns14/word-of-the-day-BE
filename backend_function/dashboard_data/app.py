import json
import os

import jwt

HEADERS = {
            'Access-Control-Allow-Headers': "*",
            'Access-Control-Allow-Origin': 'https://wordsoftheday.org',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        }


def lambda_handler(event, context):
    print(event)
    body = json.loads(event['body'])
    if body['action'] == 'dashboard_data':
        token = body['token']
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
            'body': json.dumps({'user': user_jwt['user_email']})
        }
