import json
import boto3
from botocore.exceptions import ClientError

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
    AWS Lambda handler function to authenticate a user against the DynamoDB table.

    Args:
        event (dict): The event dictionary containing the 'username' and 'password'.
        context (object): The context object containing runtime information.

    Returns:
        dict: Response object indicating success or failure of the authentication.
    """
    # Extract username and password from the event
    username = event['username']
    password = event['password']

    try:
        # Retrieve the user from the table
        response = table.get_item(Key={'username': username})

        # Check if the user exists and the password matches
        if 'Item' not in response or response['Item']['password'] != password:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps('Invalid username or password')
            }

        # Return a successful login response
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps('Login successful')
        }
    except ClientError as e:
        # Extract the error message
        error_message = e.response['Error']['Message']
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': error_message})
        }
