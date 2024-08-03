import boto3

class S3Client:
    def __init__(self):
        print('--- Creating S3 connection ---')
        self.s3_resource = boto3.client("s3")
        print('S3 connection created')

    def get_object(self, bucket, objectkey):
        obj = self.s3_resource.get_object(Bucket=bucket, Key=objectkey)
        return obj