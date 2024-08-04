import urllib.parse
import boto3

s3 = boto3.client('s3')
glue = boto3.client('glue')
glueJobName = 'superstore-sales-pipeline'

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    response = glue.start_job_run(JobName = glueJobName, Arguments={'--CSV_BUCKET': bucket, '--OBJECT_KEY': key})
    return response
