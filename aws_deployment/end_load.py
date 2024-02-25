import csv
import psycopg2
import boto3
from io import StringIO

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    
    # Retrieve the CSV file from S3
    response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    csv_file_content = response['Body'].read().decode('utf-8')
    
    # Connect to the PostgreSQL RDS database
    conn = psycopg2.connect(
        dbname='dbname',
        user='user',
        password='password',
        host='host',
        port='port'
    )
    cur = conn.cursor()
    
    # Parse the CSV file and insert each row into the database
    reader = csv.reader(StringIO(csv_file_content))
    next(reader)  # Skip the header row
    for row in reader:
        insert_query = f"INSERT INTO dashboard_raw.eod (symbol,date,open,high,low,close,adjclose,volume,unadjustedvolume,change,changepercent,vwap,label,changeovertime) VALUES ({', '.join(['%s'] * len(row))})"
        cur.execute(insert_query, row)
    
    conn.commit()
    cur.close()
    conn.close()
    
    return {
        'statusCode': 200,
        'body': 'CSV data loaded into PostgreSQL successfully.'
    }
