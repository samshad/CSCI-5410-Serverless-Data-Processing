import json
import base64
import boto3
from botocore.exceptions import ClientError

# Initialize the S3 client
s3 = boto3.client('s3')

# S3 bucket name for user profile pictures
BUCKET_NAME = 'user-profile-pictures-bucket'

# CORS headers to allow cross-origin requests
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
}


def lambda_handler(event, context):
    """
    AWS Lambda handler function to upload a user profile picture to a S3 bucket.

    Args:
        event (dict): The event dictionary containing the 'username' and 'image_data'.
        context (object): The context object containing runtime information.

    Returns:
        dict: Response object indicating success or failure of the upload operation.
    """
    # Extract username and image data from the event
    username = event['username']
    image_data = event['image_data']

    # Decode the base64 encoded image data
    image_bytes = base64.b64decode(image_data)

    # Construct the S3 object key
    key = f"profile-pictures/{username}.jpg"

    try:
        # Upload the image to S3
        s3.put_object(Bucket=BUCKET_NAME, Key=key, Body=image_bytes, ContentType='image/jpeg')

        # Return a successful response
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps('Profile picture uploaded successfully')
        }
    except ClientError as e:
        # Extract the error message
        error_message = e.response['Error']['Message']
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': error_message})
        }
