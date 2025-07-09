# AWS Lambda S3 Image Processor

## Overview

This repository contains an AWS Lambda function (`lambda-image-processor.py`) written in Python that automatically resizes images uploaded to an S3 bucket. When a new image is uploaded, the Lambda function is triggered, resizes the image to 300x300 pixels, and saves the processed image to a destination S3 bucket.



\## Features



\- \*\*Automatic image resizing:\*\* Listens for new images in a source S3 bucket and resizes them.

\- \*\*S3 integration:\*\* Downloads the original image and uploads the processed image to a separate S3 bucket.

\- \*\*Customizable output size:\*\* Easily change the target size in the code.



\## How it Works



1\. \*\*Upload an image\*\* to the specified source S3 bucket.

2\. \*\*Lambda is triggered\*\* by the S3 event.

3\. \*\*The Lambda function:\*\*

&nbsp;  - Downloads the image from S3

&nbsp;  - Resizes it to 300x300 pixels using \[Pillow](https://python-pillow.org/)

&nbsp;  - Uploads the processed image to the destination S3 bucket



\## Requirements



\- \*\*AWS Lambda\*\* with a Python runtime (Python 3.12 recommended)

\- \*\*Pillow\*\* library (must be included using a Lambda Layer or packaged with your deployment)

\- Two S3 buckets: one for source images, one for processed images



\## Setup Instructions



\### 1. Prepare the Lambda Function



\- Copy the `lambda-image-processor.py` code to your Lambda function.

\- Set the Lambda handler to:  

&nbsp; ```

&nbsp; lambda-image-processor.lambda\_handler

&nbsp; ```



\### 2. Add Pillow Library



AWS Lambda does not include Pillow by default. You must add it using one of these options:



\#### Option A: Use a Lambda Layer



\- Find a Pillow Lambda Layer compatible with your Python runtime (e.g., from \[Klayers](https://github.com/keithrozario/Klayers)).

\- Attach the Layer to your Lambda function.



\#### Option B: Bundle Pillow with Your Deployment



```bash

mkdir python

pip install Pillow -t python/

zip -r9 function.zip lambda-image-processor.py

cd python

zip -r9 ../function.zip .

```

\- Upload `function.zip` to Lambda.



\### 3. Configure S3 Triggers



\- Set your source S3 bucket to trigger the Lambda function on object creation.



\### 4. Set Destination Bucket



\- Update the destination bucket name in the code:

&nbsp; ```python

&nbsp; dest\_bucket = 'my-image-processed'

&nbsp; ```



\## Example Event



The Lambda expects an S3 event like:



```json

{

&nbsp; "Records": \[

&nbsp;   {

&nbsp;     "s3": {

&nbsp;       "bucket": {

&nbsp;         "name": "source-bucket"

&nbsp;       },

&nbsp;       "object": {

&nbsp;         "key": "image.jpg"

&nbsp;       }

&nbsp;     }

&nbsp;   }

&nbsp; ]

}

```



\## Troubleshooting



\- If you see `No module named 'PIL'`, ensure Pillow is included as a Layer or in your deployment package.

\- Check that the IAM role for your Lambda has permissions for both S3 buckets.



---



\*\*Author:\*\* \[DWeller1013](https://github.com/DWeller1013)  

\*\*Project:\*\* \[AWS\_Image\_Processing](https://github.com/DWeller1013/AWS\_Image\_Processing)

