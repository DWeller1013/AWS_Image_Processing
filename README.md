# S3 Lambda Image Processor

This AWS Lambda function automatically processes images uploaded to a source S3 bucket and saves the processed images to a destination S3 bucket. It is designed to handle a wide range of image formats and edge cases.

## Features

- **Automatic Trigger:** Invoked by S3 event notifications when a new image is uploaded to the source bucket.
- **Multi-format Support:** Handles PNG, JPEG, GIF, BMP, and other common image types.
- **Key Decoding:** Robustly decodes S3 object keys to handle spaces and special characters.
- **Transparency Handling:** Converts images with alpha channels (transparency) to RGB for JPEG compatibility.
- **Resizing:** Resizes all processed images to 300x300 pixels.
- **Consistent Output:** Saves all processed images as `.jpg` files to the destination bucket.
- **Retry Logic:** Retries S3 object retrieval to handle eventual consistency issues.
- **Logging:** Outputs helpful logs for debugging and traceability.

## How It Works

1. **Upload:** An image is uploaded to the source S3 bucket.
2. **S3 Event:** The Lambda function is triggered by the S3 `ObjectCreated` event.
3. **Processing:**
    - Downloads and decodes the object key
    - Opens the image using Pillow (PIL)
    - Converts images with transparency to RGB if saving as JPEG
    - Resizes the image to 300x300 pixels
    - Saves the processed image as a `.jpg` file
4. **Save:** The processed image is uploaded to the destination S3 bucket.

## Configuration

- **Source Bucket:** The S3 bucket that receives the original images and triggers the Lambda.
- **Destination Bucket:** The S3 bucket where processed images are saved (update the `dest_bucket` variable in the code).
- **IAM Role:** The Lambda execution role must have `s3:GetObject` permission for the source bucket and `s3:PutObject` for the destination bucket. It should also have permission to write logs to CloudWatch.

## Customization

- **Output Format:** By default, all outputs are JPEG. You can modify the code to preserve original formats or handle other output requirements.
- **Resize Dimensions:** Change the dimensions in the `resize()` call as needed.
- **Additional Processing:** Add filters, watermarks, or other Pillow operations as desired.

## Example Event

The function expects an event structured like this (from S3):

```json
{
  "Records": [
    {
      "s3": {
        "bucket": {
          "name": "your-source-bucket"
        },
        "object": {
          "key": "your%20image.png"
        }
      }
    }
  ]
}
```

## Error Handling

- If the image is not yet available (due to S3 eventual consistency), the function retries fetching it.
- If an unsupported or corrupted image is uploaded, the function logs the error and fails gracefully.

## Requirements

- Python 3.8 or newer
- [Pillow](https://python-pillow.org/) library included in your Lambda deployment package or Lambda Layer
- AWS permissions for S3 and CloudWatch Logs

## Deployment

1. Package your code (and Pillow if not using a Lambda Layer).
2. Deploy to Lambda with the appropriate handler and IAM role.
3. Set up an S3 event trigger for your source bucket.

---

**This function is robust for automation pipelines, batch processing, or as an example of image handling in AWS Lambda.**

---


**Author:** [DWeller1013](https://github.com/DWeller1013)  
**Project:** [AWS_Image_Processing](https://github.com/DWeller1013/AWS_Image_Processing)

