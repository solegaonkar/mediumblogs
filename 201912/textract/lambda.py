import json
import boto3


def lambda_handler(event, context):

    client = boto3.client('textract')
    response = client.detect_document_text( \
        Document={'S3Object': {'Bucket': "learn-textract", 'Name': "Screenshot from 2019-12-07 11-28-21.png"}})

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
