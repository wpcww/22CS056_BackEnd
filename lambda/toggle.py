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
        data = orgtable.update_item(
            Key={
                'org': oCode
            },
            UpdateExpression='SET orgstatus = :s',
            ExpressionAttributeValues={
                ':s': "accepted"
            }
        )
        # print("Organization Public Key: " + orgKey)
        response = {
            'statusCode': 200,
            'body': json.dumps(data),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Methods": "POST,GET,OPTIONS, PUT, DELETE"
            },
        }
        return response

    except Exception as e:
        print(e)
        response = {
            'statusCode': 400,
            'body': json.dumps('Failed to toggle.'),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Methods": "POST,GET,OPTIONS, PUT, DELETE"
            },
        }
        return response
