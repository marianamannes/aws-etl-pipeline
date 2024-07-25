import boto3
import pandas as pd

class S3Connector:
    def __init__(self):
        print('--- Creating S3 connection ---')
        self.s3_resource = boto3.client("s3")
        print('S3 connection created')

    def get_object(self, bucket, objectkey):
        # Convert S3 object content to dataframe
        obj = self.s3_resource.get_object(Bucket=bucket, Key=objectkey)
        df = pd.read_csv(obj['Body'], index_col=None)
        return df, len(df)