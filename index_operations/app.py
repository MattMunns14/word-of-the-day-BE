import json


def lambda_handler(event, context):
    print(event)

    return {
        "headers": {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST,GET'
        },
        "statusCode": 200,
        "body": json.dumps({
            "message": "Hi Erin!",
        }),
    }


