import boto3
from PIL import Image, UnidentifiedImageError
import io
import time
import botocore
import urllib.parse

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    src_bucket = event['Records'][0]['s3']['bucket']['name']
    raw_src_key = event['Records'][0]['s3']['object']['key']
    src_key = urllib.parse.unquote_plus(raw_src_key)
    dest_bucket = 'my-image-processed-dmw'
    output_format = 'JPEG'  # Change to None to preserve input format

    print(f"Raw key from event: {raw_src_key}")
    print(f"Decoded key: {src_key}")

    # Retry logic for eventual consistency
    for attempt in range(8):
        try:
            image_obj = s3.get_object(Bucket=src_bucket, Key=src_key)
            image_content = image_obj['Body'].read()
            break
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                print(f"Attempt {attempt+1}: Key not found, retrying...")
                time.sleep(0.75)
            else:
                raise
    else:
        print("Failed to get object after retries.")
        raise

    try:
        image = Image.open(io.BytesIO(image_content))
    except UnidentifiedImageError:
        print("ERROR: Cannot identify image file.")
        raise

    print(f"Original format: {image.format}, mode: {image.mode}")

    # Convert to RGB if needed (for JPEG, or to remove alpha for other formats)
    if output_format == 'JPEG':
        if image.mode in ('RGBA', 'LA', 'P'):
            image = image.convert('RGB')
        save_format = 'JPEG'
        processed_key = src_key.rsplit('.', 1)[0] + '.jpg'
        content_type = 'image/jpeg'
    else:
        # Preserve original format
        save_format = image.format if image.format else 'PNG'
        processed_key = src_key
        content_type = f'image/{save_format.lower()}'

        # For non-JPEG formats, convert palette or alpha to RGB or RGBA as needed
        if save_format == 'PNG':
            if image.mode == 'P':
                image = image.convert('RGBA')
        elif save_format == 'GIF':
            if image.mode not in ('L', 'P'):
                image = image.convert('P')

    # Resize if desired
    image = image.resize((300, 300))

    buffer = io.BytesIO()
    image.save(buffer, format=save_format)
    buffer.seek(0)

    s3.put_object(
        Bucket=dest_bucket,
        Key=processed_key,
        Body=buffer,
        ContentType=content_type
    )
    print(f"Image processed and uploaded as {processed_key} ({content_type})")
    return {'statusCode': 200, 'body': f'Image processed as {processed_key}'}