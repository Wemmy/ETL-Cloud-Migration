import boto3
import json

class S3Writer:
    def __init__(self, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, aws_session_token=None):
        """
        Initialize the S3 client.

        Parameters:
        aws_access_key_id (str): AWS access key id.
        aws_secret_access_key (str): AWS secret access key.
        aws_session_token (str, optional): AWS session token (if any).
        """
        # Initialize a session using your credentials
        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_session_token=aws_session_token
        )

        # Initialize the S3 client
        self.s3_client = session.client('s3')

    def write_json_to_s3(self, data, bucket_name, file_name):
        """
        Write JSON data to a file in an S3 bucket using the initialized client.

        Parameters:
        data (dict): JSON data to write.
        bucket_name (str): Name of the S3 bucket.
        file_name (str): File name to be used in the S3 bucket.

        Returns:
        None
        """
        # Convert the data to JSON
        json_data = json.dumps(data)

        # Write the JSON data to the specified S3 bucket
        self.s3_client.put_object(Body=json_data, Bucket=bucket_name, Key=file_name)

