
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import explode, col
from datetime import datetime,timedelta,timezone
from pyspark.sql.functions import explode, col
import boto3
from botocore.exceptions import ClientError
from pyspark.sql.utils import AnalysisException
  
sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
current_date = datetime.now()
# Calculate yesterday's date
yesterday_date = (current_date - timedelta(days=2)).strftime('%Y-%m-%d')
month = current_date.strftime('%Y-%m')
KEY = (
    yesterday_date
)
print(KEY)
s3 = boto3.client('s3')
input_eod_path = f"s3://dashboard-team-bucket-1/{month}/{KEY}/eod/"
output_eod_path = f"s3://dashboard-team-bucket-2/{month}/{KEY}/eod/"
try:
    # Proceed with reading the file as it exists
    df = spark.read.json(input_eod_path)
    print("File exists")
    df = df.select(
            explode("historical").alias("historical"),
            "symbol"
        ).select(
            "symbol",
            "historical.date",
            "historical.open",
            "historical.high",
            "historical.low",
            "historical.close",
            "historical.adjClose",
            "historical.volume",
            "historical.unadjustedVolume",
            "historical.change",
            "historical.changePercent",
            "historical.vwap",
            "historical.label",
            "historical.changeOverTime"
        ).withColumnRenamed("symbol", "Symbol")
    
    # Write the result to CSV
    df.coalesce(1).write.mode("overwrite").option("header", "true").csv(output_eod_path)
    
    # reanme the file
    response = s3.list_objects(
        Bucket = 'dashboard-team-bucket-2',
        Prefix = f'{month}/{KEY}/eod/',
        Delimiter='/'
    )
    name = response["Contents"][0]["Key"]
    print(name)

    ## Store Target File File Prefix, this is the new name of the file
    target_source = {'Bucket': 'dashboard-team-bucket-2', 'Key': name}
    s3.copy(Bucket='dashboard-team-bucket-2', CopySource=target_source,  Key=f'{month}/{KEY}/eod/eod.csv')
    s3.delete_object(Bucket='dashboard-team-bucket-2', Key=name)
except AnalysisException as e:
    if "Path does not exist" in str(e):
        print("Specified path does not exist in S3")
    else:
        raise  # Re-throw exception if it's not a path issue
if current_date.day == 1:
    folder_names = ['balance_sheet_statement',
                    'cashflow_statement',
                    'income_statement',
                    'key_metrics'
                    ]
    for folder in folder_names:
        input_path = f"s3://dashboard-team-bucket-1/metrics/{folder}/"
        output_path = f"s3://dashboard-team-bucket-2/metrics/{folder}/"

        df = spark.read.json(input_path)

        # Write the result to CSV
        df.write.mode("overwrite").option("header", "true").csv(output_path)

    files = [
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
    for file in files:
        input_path = f"s3://dashboard-team-bucket-1/metrics/{file}"
        output_path = f"s3://dashboard-team-bucket-2/metrics/{file}"

        dynamic_frame = glueContext.create_dynamic_frame.from_options(
            connection_type="s3",
            connection_options={"paths": [input_path]},
            format="json"
        )

        data_dynamic_frame = dynamic_frame.select_fields(['data'])

        df = data_dynamic_frame.toDF()

        # Explode the 'data' array to create a row for each element and select 'date' and 'value'
        df_transformed = df.select(explode("data").alias("data")).select(
            col("data.date").alias("date"),
            col("data.value").alias("value")
        )
        # Convert back to DynamicFrame
        dyf_transformed = DynamicFrame.fromDF(df_transformed, glueContext, "dyf_transformed")

        # Write the transformed DynamicFrame to CSV
        glueContext.write_dynamic_frame.from_options(
            frame=dyf_transformed,
            connection_type="s3",
            connection_options={"path": output_path},
            format="csv",
            format_options={"writeHeader": True}
        )
job.commit()