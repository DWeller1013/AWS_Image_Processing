import boto3
from PIL import Image
import io

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    # Get event info
    src_bucket = event['Records'][0]['s3']['bucket']['name']
    src_key = event['Records'][0]['s3']['object']['key']
    dest_bucket = 'my-image-processed'  # Change to your destination bucket

    # Download image from S3
    image_obj = s3.get_object(Bucket=src_bucket, Key=src_key)
    image_content = image_obj['Body'].read()
    image = Image.open(io.BytesIO(image_content))

    # Process image (resize)
    image = image.resize((300, 300))
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG')
    buffer.seek(0)

    # Upload processed image to destination bucket
    s3.put_object(Bucket=dest_bucket, Key=src_key, Body=buffer, ContentType='image/jpeg')

    return {'statusCode': 200, 'body': 'Image processed'}
