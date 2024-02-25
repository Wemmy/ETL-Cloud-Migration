import csv
import psycopg2
import boto3
from io import StringIO
import json

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    bucket_name = 'dashboard-team-bucket-2'
    prefix = 'metrics/'
    
    folder_names = [
        'balance_sheet_statement',
        'cashflow_statement',
        'income_statement',
        'key_metrics',
        'real_gdp.json',
        'real_gdp_per_capita.json',
        'treasury_yield.json',
        'fed_fund_rate.json',
        'cpi.json',
        'inflation.json',
        'retail_sales.json',
        'durables.json',
        'unemployment_rate.json',
        'nonfarm_payroll.json'
    ]
    
    # Connect to the PostgreSQL RDS database
    conn = psycopg2.connect(
        dbname='dbname',
        user='user',
        password='password',
        host='host',
        port='port'
    )
    cur = conn.cursor()
    
    # Retrieve the CSV file from S3
    for folder in folder_names:
        # List all files in the Glue job output prefix
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix + f'{folder}/')
        if 'Contents' in response:
            
            # get table's name
            table_name = folder.split('.')[0]
            
            
            # Drop the table
            cur.execute(f"DROP TABLE IF EXISTS dashboard_raw.{table_name}")
            

            for idx, obj in enumerate(response['Contents']):
                file_key = obj['Key']
                csv_file = s3_client.get_object(Bucket=bucket_name, Key=file_key)
                csv_content = csv_file['Body'].read().decode('utf-8')
                csv_reader = csv.reader(StringIO(csv_content))
                if idx == 0:
                    header = next(csv_reader)
                    # create table 
                    cur.execute(f"CREATE TABLE dashboard_raw.{table_name} ({', '.join([col + ' TEXT' for col in header])});")
                    for row in csv_reader:
                        # Adjust SQL query as needed
                        cur.execute(f"INSERT INTO dashboard_raw.{table_name} VALUES ({', '.join(['%s'] * len(row))});", row)
                else:
                    next(csv_reader)  # Skip header row if present
                    for row in csv_reader:
                        # Adjust SQL query as needed
                        cur.execute(f"INSERT INTO dashboard_raw.{table_name} VALUES ({', '.join(['%s'] * len(row))});", row)
        else:
            print("No files found.")
                

    
    conn.commit()
    cur.close()
    conn.close()
    
    return {
        'statusCode': 200,
        'body': 'CSV data loaded into PostgreSQL successfully.'
    }

