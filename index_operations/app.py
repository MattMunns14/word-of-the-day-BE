import json


def lambda_handler(event, context):
    print(event)

    return {
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': 'https://wordsoftheday.org',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "statusCode": 200,
        "body": json.dumps({
            "message": "Hi Erin!",
        }),
    }


