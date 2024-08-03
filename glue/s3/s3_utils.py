import pandas as pd

def get_s3_obj_df(s3_client, bucket, objectkey):
    obj = s3_client.get_object(bucket, objectkey)
    df = pd.read_csv(obj['Body'], index_col=None)
    return df

def get_s3_obj_string(s3_client, bucket, objectkey):
    obj = s3_client.get_object(bucket, objectkey)
    obj_string = obj['Body'].read().decode('utf-8')
    return obj_string