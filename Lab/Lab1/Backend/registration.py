import json
import boto3
from botocore.exceptions import ClientError
import hashlib

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Specify the DynamoDB table
table = dynamodb.Table('Users')

# CORS headers to allow cross-origin requests
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
}


def lambda_handler(event, context):
    """
    AWS Lambda handler function to register a new user into the DynamoDB table.

    Args:
        event (dict): The event dictionary containing the 'username' and 'password'.
        context (object): The context object containing runtime information.

    Returns:
        dict: Response object indicating success or failure of the operation.
    """
    # Extract username and password from the event
    username = event['username']
    password = event['password']

    # Hash the password using MD5
    password = hashlib.md5(password.encode()).hexdigest()

    # Check if the user already exists in the table
    try:
        response = table.get_item(Key={'username': username})
        if 'Item' in response:
            # User already exists
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps('User already exists')
            }
    except ClientError as e:
        # Log the error message and return a server error response
        error_message = e.response['Error']['Message']
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': error_message})
        }

    # Add the new user to the table
    try:
        table.put_item(Item={'username': username, 'password': password})
        # Return a successful response
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps('User registered successfully')
        }
    except ClientError as e:
        # Log the error message and return a server error response
        error_message = e.response['Error']['Message']
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': error_message})
        }
