import unittest
from unittest.mock import patch, MagicMock
import json
from feedbacks_crud import lambda_handler, generate_uuid

# Mock UUID
mock_uuid = "123e4567-e89b-12d3-a456-426614174000"


class TestLambdaFunction(unittest.TestCase):
    """
    Test suite for the AWS Lambda function handling feedback CRUD operations.
    """

    @patch('feedbacks_crud.dynamodb_table')
    def test_status_check(self, mock_dynamodb_table):
        """
        Test the status check endpoint.
        """
        event = {
            'httpMethod': 'GET',
            'path': '/status'
        }
        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['body'], json.dumps('Service is operational'))

    @patch('feedbacks_crud.dynamodb_table')
    def test_get_feedback_by_id(self, mock_dynamodb_table):
        """
        Test retrieving feedback by feedback_id.
        """
        mock_dynamodb_table.get_item.return_value = {
            'Item': {
                'feedback_id': '101',
                'feedback': 'Test feedback',
                'username': 'testuser',
                'Date_time': '2022-09-03 12:32:24'
            }
        }
        event = {
            'httpMethod': 'GET',
            'path': '/feedback',
            'body': json.dumps({'feedback_id': '101'})
        }
        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Test feedback', response['body'])

    @patch('feedbacks_crud.dynamodb_table')
    def test_get_feedback_by_user(self, mock_dynamodb_table):
        """
        Test retrieving feedback by username.
        """
        mock_dynamodb_table.query.return_value = {
            'Items': [
                {
                    'feedback_id': '101',
                    'feedback': 'Test feedback',
                    'username': 'testuser',
                    'Date_time': '2022-09-03 12:32:24'
                }
            ]
        }
        event = {
            'httpMethod': 'GET',
            'path': '/feedback',
            'body': json.dumps({'username': 'testuser'})
        }
        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Test feedback', response['body'])

    @patch('feedbacks_crud.dynamodb_table')
    def test_get_feedbacks(self, mock_dynamodb_table):
        """
        Test retrieving all feedbacks.
        """
        mock_dynamodb_table.scan.return_value = {
            'Items': [
                {
                    'feedback_id': '101',
                    'feedback': 'Test feedback',
                    'username': 'testuser',
                    'Date_time': '2022-09-03 12:32:24'
                }
            ]
        }
        event = {
            'httpMethod': 'GET',
            'path': '/feedbacks'
        }
        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Test feedback', response['body'])

    @patch('feedbacks_crud.generate_uuid', return_value=mock_uuid)
    @patch('feedbacks_crud.dynamodb_table')
    def test_save_feedback(self, mock_dynamodb_table, mock_generate_uuid):
        """
        Test saving new feedback.
        """
        event = {
            'httpMethod': 'POST',
            'path': '/feedback',
            'body': json.dumps({
                'feedback': 'New feedback',
                'username': 'newuser',
                'Date_time': '2022-09-03 12:32:24'
            })
        }
        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Feedback added successfully', response['body'])


if __name__ == '__main__':
    unittest.main()
