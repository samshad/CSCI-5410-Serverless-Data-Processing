import json
import boto3
from botocore.exceptions import ClientError
import base64

"""
session = boto3.session.Session(
    aws_access_key_id="",
    aws_secret_access_key="",
    aws_session_token="")
"""

# Initialize the S3 client
s3 = boto3.client('s3')

# S3 bucket name containing the compressed profile pictures for retrieval
BUCKET_NAME = 'compressed-profile-pictures'

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# CORS headers to allow cross-origin requests
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
}


def lambda_handler(event, context):
    """
    AWS Lambda handler function to retrieve a resized profile picture from S3 and return it as a base64 encoded string.

    Args:
        event (dict): The event dictionary containing the 'username'.
        context (object): The context object containing runtime information.

    Returns:
        dict: Response object containing the base64 encoded image data or an error message.
    """
    # Extract username from the event
    username = event['username']

    # Construct the S3 object key
    key = f"resized-profile-pictures/{username}.jpg"

    try:
        # Retrieve the object from S3
        response = s3.get_object(Bucket=BUCKET_NAME, Key=key)

        # Read the image data and encode it as a base64 string
        image_data = base64.b64encode(response['Body'].read()).decode('utf-8')

        # Specify the DynamoDB table
        table = dynamodb.Table('image-size-status')

        # Retrieve the image status from DynamoDB
        result = table.get_item(Key={"Image": username + ".jpg"})["Item"]
        before_size = f"{result['before_size']:.2f} KB"
        after_size = f"{result['after_size']:.2f} KB"
        image_status = (result["Image"], before_size, after_size)

        # Return a successful response with the image data
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'image_data': image_data, 'image_status': image_status})
        }
    except ClientError as e:
        # Extract the error message
        error_message = e.response['Error']['Message']

        # Return an error response
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': error_message})
        }

