import json
import boto3
from decimal import Decimal

# Initialize AWS clients
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

# DynamoDB table name
table_name = 'dashboard_news'
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    # Get bucket name and file key from the S3 event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    
    # Get the JSON file content
    file_obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    file_content = file_obj['Body'].read().decode('utf-8')
    # Replace 'file_content' with your actual string content from S3
    json_content = json.loads(file_content, parse_float=Decimal)
    
    # Process only the 'feed' data
    feed_data = json_content.get('feed', [])
    
    for item in feed_data:
        # Assuming each item in 'feed' is a dictionary that matches your DynamoDB table schema
        table.put_item(Item=item)
        
    
    return {
        'statusCode': 200,
        'body': json.dumps('Successfully processed and loaded feed data to DynamoDB.')
    }
