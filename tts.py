import json
import boto3
import requests


BACKET="3d-avatar"

session = boto3.session.Session()
s3 = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net'
)


def synthesize(text, iam_token, lang='ru-RU', is_male=True):
    url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
    headers = {
        'Authorization': 'Bearer ' + iam_token,
    }
    
    voice = 'filipp'
    if lang != 'ru-RU':
        voice = 'john'
    
    if not is_male:
        voice = 'alena'

    data = {
        'text': text,
        'lang': lang,
        'voice': voice,
        'folderId': 'b1gviik7gicnqdmq2fiu',
        'sampleRateHertz': 48000,
    }

    with requests.post(url, headers=headers, data=data, stream=True) as resp:
        if resp.status_code != 200:
            raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))

        for chunk in resp.iter_content(chunk_size=None):
            yield chunk


def handler(event, context):
    try:
        # Check if request method is POST
        if event['httpMethod'] != 'POST':
            return {
                'statusCode': 400,
                'body': 'Only a POST request with `Content-Type: application/json` is supported',
            }

        # Parse JSON from request body
        body = json.loads(event['body'])
        # get iam token from contex
        iam_token = context.token['access_token']

        # Check if required fields are present in the request body
        required_fields = ['text', 'clientId']
        for field in required_fields:
            if field not in body:
                return {
                    'statusCode': 400,
                    'body': f'Missing required field: {field}',
                }

        text = body['text']
        clientId = body['clientId']
        lang = body.get('lang', 'ru-RU')
        is_male = body.get('isMale', True)

        # Create a file-like object to write the synthesized audio to
        with open('/tmp/synthesized_audio.ogg', 'wb') as f:
            for audio_chunk in synthesize(text, iam_token, lang, is_male):
                f.write(audio_chunk)

        # Upload the synthesized audio to Yandex Object Storage
        s3.upload_file('/tmp/synthesized_audio.ogg', BACKET, f'{clientId}.ogg', ExtraArgs={'ACL': 'public-read', 'ContentType': 'audio/ogg'})
        
        # get url of uploaded file
        url = s3.generate_presigned_url('get_object', Params={'Bucket': BACKET, 'Key': f'{clientId}.ogg'}, ExpiresIn=3600)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'url': url
            }),
        }
    except Exception as e:
        print(e)
        # Return a 500 error with the exception message
        return {
            'statusCode': 500,
            'body': str(e),
        }