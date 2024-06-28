import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

# Create a DynamoDB resource
dynamodb = boto3.resource('dynamodb')
dynamodb_table = None

# Define paths for different operations
STATUS_CHECK_PATH = '/status'
FEEDBACK_PATH = '/feedback'
FEEDBACKS_PATH = '/feedbacks'


def lambda_handler(event, context):
    """
    Main handler function for the AWS Lambda.

    Args:
    event (dict): The event data containing HTTP method and parameters.
    context (object): The runtime information of the Lambda function.

    Returns:
    dict: Response containing status code and message or data.
    """
    print('Request event: ', event)
    response = None

    # Get the DynamoDB table name from the request body and create a DynamoDB table resource
    table_name = json.loads(event['body'])['db_table_name']
    global dynamodb_table
    dynamodb_table = dynamodb.Table(table_name)

    try:
        http_method = event.get('httpMethod')
        path = event.get('path')

        if http_method == 'GET' and path == STATUS_CHECK_PATH:
            response = build_response(200, 'Service is operational')
        elif http_method == 'GET' and path == FEEDBACK_PATH:
            response = get_feedback(json.loads(event['body']))
        elif http_method == 'GET' and path == FEEDBACKS_PATH:
            response = get_feedbacks()
        elif http_method == 'POST' and path == FEEDBACK_PATH:
            response = save_feedback(json.loads(event['body']))
        else:
            response = build_response(404, '404 Not Found')

    except Exception as e:
        print('Error:', e)
        response = build_response(400, 'Error processing request')

    return response


def get_feedback(body):
    """
    Get feedback by its ID or user.

    Args:
    body (dict): The request body containing the feedback ID or user.

    Returns:
    dict: A response with the feedback data.
    """
    try:
        feedback_id = body.get('feedback_id')
        feedback_user = body.get('username')

        if feedback_id:
            return get_feedback_by_id(feedback_id)
        elif feedback_user:
            return get_feedback_by_user(feedback_user)
        else:
            return build_response(400, 'Invalid request: Missing feedback_id or username')
    except ClientError as e:
        print('Error:', e)
        return build_response(500, 'Error getting feedback')


def get_feedback_by_id(feedback_id):
    """
    Get feedback by its ID.

    Args:
    feedback_id (str): The ID of the feedback to retrieve.

    Returns:
    dict: A response with the feedback data.
    """
    try:
        response = dynamodb_table.get_item(Key={'feedback_id': feedback_id})
        feedback = response.get('Item', {})
        return build_response(200, feedback)
    except ClientError as e:
        print('Error:', e)
        return build_response(500, 'Error getting feedback')


def get_feedback_by_user(feedback_user):
    """
    Get feedback by its user.

    Args:
    feedback_user (str): The username to retrieve feedback for.

    Returns:
    dict: A response with the feedback data.
    """
    try:
        response = dynamodb_table.query(
            IndexName='username-index',
            KeyConditionExpression=Key('username').eq(feedback_user)
        )
        feedback = response.get('Items', [])
        return build_response(200, feedback)
    except ClientError as e:
        print('Error:', e)
        return build_response(500, 'Error getting feedback')


def get_feedbacks():
    """
    Get all feedbacks from the database.

    Returns:
    dict: A response with a list of feedbacks.
    """
    try:
        response = dynamodb_table.scan()
        feedbacks = response.get('Items', [])
        return build_response(200, feedbacks)
    except ClientError as e:
        print('Error:', e)
        return build_response(500, 'Error getting feedbacks')


def save_feedback(feedback_data):
    """
    Save new feedback to the database.

    Args:
    feedback_data (dict): The feedback data to save.

    Returns:
    dict: A response indicating success or failure.
    """
    try:
        dynamodb_table.put_item(Item=feedback_data)
        return build_response(200, 'Feedback added successfully')
    except ClientError as e:
        print('Error:', e)
        return build_response(500, 'Error saving feedback')


def build_response(status_code, body):
    """
    Build an HTTP response.

    Args:
    status_code (int): The HTTP status code.
    body (dict or list): The body of the response to be converted to JSON.

    Returns:
    dict: The HTTP response with the specified status code and body.
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body)
    }
