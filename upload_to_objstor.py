import boto3
import os

session = boto3.session.Session()

ENDPOINT = "https://storage.yandexcloud.net"
BACKET = "3d-avatar"

session = boto3.Session(
    aws_access_key_id=(os.environ['token']),
    aws_secret_access_key=(os.environ['key_value']),
    region_name="ru-central1",
)

s3 = session.client(
    service_name='s3',
    endpoint_url=ENDPOINT
)

def upload_to_storage(path, client_id):
    s3.upload_file(path, BACKET, f'{client_id}.mp4', ExtraArgs={'ACL': 'public-read', 'ContentType': 'audio/mp4'})
        
