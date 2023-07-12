import json
import boto3
import os
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
import hashlib

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    # Read API parameters: verification record, org name, vac id
    body = json.loads(event['body'])
    vr = body['vr']
    orgName = body['org']
    vid = body['vid']
    vrec_ddb = os.environ['TABLE_NAME']

    table = dynamodb.Table(vrec_ddb)
    try:
        # Search table for vrecord id = vid, retrieve the whole record
        data = table.query(
            KeyConditionExpression=Key('id').eq(vid)
        )

        # Retrieve pid
        pid = data['Items'][0]['pid']
        # Check if pid match with hashed vr
        hashobj = hashlib.sha256()
        hashobj.update(bytes(vr, encoding='utf-8'))
        # if pid != hashobj.hexdigest():
        #   raise ValueError

        # Return response with the vaccination details
        response = {
            'statusCode': 200,
            'body': json.dumps({
                "info": data['Items'][0]['info'],
                "sign": data['Items'][0]['sign']

            }),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Methods": "POST,GET,OPTIONS, PUT, DELETE"
            },
        }
        return response
    except ClientError as e:
        response = {
            'statusCode': 200,
            'body': json.dumps("Invalid input, please try again."),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Methods": "POST,GET,OPTIONS, PUT, DELETE"
            },
        }
        return response
    except ValueError as e:
        response = {
            'statusCode': 200,
            'body': json.dumps("Identity does not match vaccination record."),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Methods": "POST,GET,OPTIONS, PUT, DELETE"
            },
        }
        return response
