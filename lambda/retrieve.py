import json
import boto3
import os
from boto3.dynamodb.conditions import Key
from datetime import date

today = date.today()
dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    # Read API parameters: verification record and already encrypted vac details
    body = json.loads(event['body'])
    oCode = body['oCode']
    org_ddb = os.environ['TABLE_NAME']

    # Query org_ddb to retrieve the corresponding public key
    orgtable = dynamodb.Table(org_ddb)
    try:
        data = orgtable.query(
            KeyConditionExpression=Key('org').eq(oCode)
        )
        orgKey = data['Items'][0]['pustr']
        # print("Organization Public Key: " + orgKey)
        response = {
            'statusCode': 200,
            'body': json.dumps(orgKey),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
        }
        return response

    except Exception as e:
        response = {
            'statusCode': 400,
            'body': json.dumps("Fail to retrieve organization information."),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
        }
        return response
