import boto3

BACKET = "3d-avatar"

session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)

def object_exist(key):
    try:
        s3.head_object(Bucket=BACKET, Key=key)
    except Exception as e:
        return False
    return True

def handler(event, context):
    try:
        if event['httpMethod'] != 'GET':
            return {
                'statusCode': 400,
                'body': 'Only a GET request is supported',
            }
        query = event['queryStringParameters']
        if 'file' not in query:
            return {
                'statusCode': 400,
                'body': 'Missing required field: file',
            }
        fileName = query['file']
        if not object_exist(fileName):
            return {
                'statusCode': 404,
                'body': f'File {fileName} not found',
            }
        return {
            'statusCode': 200,
            'body': 'File exists',
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': str(e),
        }