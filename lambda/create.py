import json
import boto3
import hashlib
import uuid
import os
from boto3.dynamodb.conditions import Key
from datetime import date

today = date.today()
dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    # Read API parameters: verification record and already encrypted vac details
    body = json.loads(event['body'])
    vr = body['vr']
    info = body['info']
    sign = body['sign']
    vrec_ddb = os.environ['TABLE_NAME']
    # Generate uuid for the new record
    vid = uuid.uuid4().hex
    # Hash personal info
    hashobj = hashlib.sha256()
    hashobj.update(bytes(vr, encoding='utf-8'))
    pid = hashobj.hexdigest()
    # Interact with DDB and insert new record
    table = dynamodb.Table(vrec_ddb)
    table.put_item(
        Item={
            'id': vid,
            'pid': pid,
            'date': str(today),
            'info': info,
            'sign': sign
        }
    )
    # return the created vid to the API
    response = {
        'statusCode': 200,
        'body': json.dumps(vid),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            "Access-Control-Allow-Methods": "POST,GET,OPTIONS, PUT, DELETE"
        },
    }
    return response
