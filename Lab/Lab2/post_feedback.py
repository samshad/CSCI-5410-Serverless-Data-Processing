import functions_framework
import firebase_admin
from firebase_admin import credentials, firestore
import json

# Initialize Firestore DB
cred = credentials.Certificate('Auth.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


@functions_framework.http
def hello_http(request):
    """
    HTTP Cloud Function to handle incoming requests.
    Supports only POST requests to create new feedback entries in Firestore.

    Args:
        request (flask.Request): The request object.

    Returns:
        dict: Response message with status code.
    """
    try:
        if request.method == 'POST':
            json_data = request.get_json(force=True, silent=True, cache=True)

            if not json_data or 'username' not in json_data or 'feedback' not in json_data:
                return {'message': 'Invalid request payload!!!'}, 400

            print("Username:", json_data['username'])
            print("Feedback:", json_data['feedback'])

            data = {
                "username": json_data['username'],
                "feedback": json_data['feedback']
            }

            return create_data('feedbacks', data)
        else:
            return {'message': 'Method Not Allowed!'}, 405
    except Exception as e:
        print('Error:', e)
        return {'message': f'Error processing request: {str(e)}!!!'}, 500


def create_data(collection_name, data):
    """
    Create a new document in the specified Firestore collection.

    Args:
        collection_name (str): The name of the Firestore collection.
        data (dict): The data to be stored in the Firestore document.

    Returns:
        dict: Response message with status code.
    """
    try:
        db.collection(collection_name).document().set(data)
        return {'message': 'Data created successfully!'}, 200
    except Exception as e:
        print('Error:', e)
        return {'message': f'Error creating data: {str(e)}!!!'}, 500
