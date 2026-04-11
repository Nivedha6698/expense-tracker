import boto3
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

#S3_BUCKET = 'trackercsvbucket'
#REGION = 'ap-southeast-2'  # change if needed

S3_BUCKET = os.getenv("AWS_BUCKET_NAME")
REGION = os.getenv("AWS_REGION")

s3 = boto3.client(
    's3',
    #aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    #aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    region_name=REGION
)

def upload_csv_to_s3(file_content, user_id):
    filename =  f"exports/user_{user_id}/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    s3.put_object(
        Bucket=S3_BUCKET,
        Key=filename,
        Body=file_content,
        ContentType='text/csv'
    )

    return filename


def generate_download_url(file_key):
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': S3_BUCKET, 'Key': file_key},
        ExpiresIn=3600  # 1 hour
    )
    return url