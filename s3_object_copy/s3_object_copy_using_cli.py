import subprocess
import json

def run_aws_cli_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout, stderr

def aws_sts_configure(credentials):
    stdout,stderr=run_aws_cli_command(credentials)
    if stderr:
        print("An error occured: ", stderr)
    else:
        print("command output: ", stdout)

aws_cli_command1 = "aws sts assume-role --role-arn arn:aws:iam::081063778907:role/lambda-ddb-role --role-session-name cross_acct_lambda --profile default"
stdout, stderr = run_aws_cli_command(aws_cli_command1)
if stderr:
    print("An error occurred1:", stderr)
else:
    credentials=json.loads(stdout.decode('utf-8'))
    AccessKey=credentials['Credentials']["AccessKeyId"]
    SecretAccessKey=credentials['Credentials']["SecretAccessKey"]
    SessionToken=credentials['Credentials']["SessionToken"]
    print("Command output1:", type(credentials))

set_access_key=f"aws configure --profile sts set aws_access_key_id {AccessKey}"
set_secret_key=f"aws configure --profile sts set aws_secret_access_key {SecretAccessKey}"
set_access_token=f"aws configure --profile sts set aws_session_token {SessionToken}"
aws_sts_configure(set_access_key)
aws_sts_configure(set_secret_key)
aws_sts_configure(set_access_token)

aws_cli_command2 = "aws s3 cp s3://converz-dev-backend-sea/processed_media/ s3://test.getdecode.io/ --recursive --profile sts"
stdout, stderr = run_aws_cli_command(aws_cli_command2)
if stderr:
    print("An error occurred2:", stderr)
else:
    print("Command output2:", stdout)


