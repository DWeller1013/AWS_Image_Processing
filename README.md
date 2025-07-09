# AWS Lambda S3 Image Resizer

This project provides an AWS Lambda function (`lambda-image-processor.py`) written in Python that automatically resizes images uploaded to a source S3 bucket. When a new image file appears in the bucket, the Lambda function is triggered, resizes the image to 300x300 pixels, and saves the processed image to a destination S3 bucket.

## Features

- **Automatic image resizing:** On new uploads, images are resized to 300x300 pixels.
- **Seamless S3 integration:** Handles both download from the source bucket and upload to the destination bucket.
- **Easily customizable:** You can adjust the target size by modifying the code.

## How It Works

1. An image is uploaded to the **source S3 bucket**.
2. An **S3 event** triggers the Lambda function.
3. The Lambda function:
    - Downloads the uploaded image from S3
    - Resizes it with the [Pillow](https://python-pillow.org/) library
    - Uploads the resized image to the **destination S3 bucket**

## Requirements

- AWS Lambda (Python 3.12 runtime recommended)
- The [Pillow](https://pypi.org/project/Pillow/) library (included in your deployment package)
- Two S3 buckets: one for source images, one for processed images
- Appropriate IAM permissions for S3 access

## Deployment Instructions

### 1. Prepare the Lambda Function

- Place your function code in `lambda-image-processor.py`.

### 2. Bundle Pillow with Your Code

Install Pillow and create a deployment zip:

```bash
mkdir package
pip install Pillow -t package/
cp lambda-image-processor.py package/
cd package
zip -r ../lambda-image-processor.zip .
```

### 3. Upload the Deployment Package

Upload `lambda-image-processor.zip` to your Lambda function using either the AWS Console or AWS CLI:

```bash
aws lambda update-function-code \
  --function-name <your-lambda-name> \
  --zip-file fileb://lambda-image-processor.zip
```

### 4. Set the Handler

Set the handler to:

```
lambda-image-processor.lambda_handler
```

### 5. Configure the S3 Trigger

Set your source S3 bucket to trigger the Lambda function on object creation events.

### 6. Set the Destination Bucket

Edit the code to specify your destination bucket:

```python
dest_bucket = 'my-image-processed'
```

## Example S3 Event

This function expects an S3 event of the following format:

```json
{
  "Records": [
    {
      "s3": {
        "bucket": {
          "name": "source-bucket"
        },
        "object": {
          "key": "image.jpg"
        }
      }
    }
  ]
}
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for more details.

---


**Author:** [DWeller1013](https://github.com/DWeller1013)  
**Project:** [AWS_Image_Processing](https://github.com/DWeller1013/AWS_Image_Processing)

