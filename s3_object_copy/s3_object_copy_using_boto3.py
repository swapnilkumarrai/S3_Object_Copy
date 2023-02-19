import boto3

session = boto3.Session(profile_name="default")
source_s3 = session.client("s3")

def copying_folder_from_s3(bucket_name, s3_folder_path):
    global result
    global source_bucket_name
    global source_folder_path
    source_folder_path=s3_folder_path
    source_bucket_name=bucket_name
    result = source_s3.list_objects_v2(Bucket=source_bucket_name, Prefix=source_folder_path)

sts = session.client("sts")
response = sts.assume_role(
    RoleArn="arn:aws:iam::081063778907:role/lambda-ddb-role",
    RoleSessionName="cross_acct_lambda"
)

AccessKey=response['Credentials']["AccessKeyId"]
SecretAccessKey=response['Credentials']["SecretAccessKey"]
SessionToken=response['Credentials']["SessionToken"]

new_session = boto3.Session(aws_access_key_id=AccessKey,
                      aws_secret_access_key=SecretAccessKey,
                      aws_session_token=SessionToken)                   
target_s3= new_session.client("s3")
# target_s3 = boto3.client('s3',aws_access_key_id=Access_key,
#     aws_secret_access_key=Secret_key,
#     aws_session_token=Session_key)

def pasting_folder_to_s3(bucket_name, s3_folder_path):
    target_bucket_name=bucket_name
    target_folder_path=s3_folder_path
    for obj in result.get("Contents"):
        source_key = obj['Key']
        target_key = source_key.replace(source_folder_path, target_folder_path)
        copy_source = {'Bucket': source_bucket_name, 'Key': source_key}
        target_s3.copy_object(Bucket=target_bucket_name, CopySource=copy_source, Key=target_key)


copying_folder_from_s3('converz-dev-backend-sea', 'processed_media/')
pasting_folder_to_s3('test.getdecode.io','')