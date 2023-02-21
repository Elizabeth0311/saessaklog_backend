import boto3
import logging
from botocore.exceptions import ClientError
from werkzeug.utils import secure_filename
from config import ACCES_KEY_ID, SECRET_ACCEES_KEY, S3_BUCKET_REGION
import os



def s3_connection() :
    try : 
        s3 = boto3.client(
            service_name = 's3',
            region_name = S3_BUCKET_REGION,
            aws_access_key_id = ACCES_KEY_ID,
            aws_secret_access_key = SECRET_ACCEES_KEY,
    )
    except Exception as e :
        print(e)
    else : 
        print("s3 bucket connected!")
        return s3


def upload_file_to_s3(s3, bucket, file, filename) :
    try :
        s3.put_object(
            Body = file,
            Bucket = bucket,
            Key = f'image/{filename}',
            ContentType = file.content_type,
            ACL = "public-read" #공개범위설정
        )

    except Exception as e :
        print(e)
        return  False
    return True
