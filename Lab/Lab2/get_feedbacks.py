import functions_framework
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firestore DB
cred = credentials.Certificate('Auth.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


@functions_framework.http
def hello_http(request):
    """
    HTTP Cloud Function to handle incoming requests.
    Supports only GET requests to retrieve all feedback entries from Firestore.

    Args:
        request (flask.Request): The request object.

    Returns:
        dict: Response message with status code.
    """
    try:
        if request.method == 'GET':
            return get_feedbacks()
        else:
            return {'message': 'Method Not Allowed!'}, 405
    except Exception as e:
        print('Error:', e)
        return {'message': f'Error processing request: {str(e)}!!!'}, 500


def get_feedbacks():
    """
    Get all the feedbacks from Firestore.

    Returns:
        dict: Response message with status code.
    """
    try:
        feedbacks = read_all_data('feedbacks')

        data = []
        for feedback in feedbacks:
            data.append(feedback.to_dict())

        return {'feedbacks': data}, 200
    except Exception as e:
        print('Error:', e)
        return {'message': f'Error processing request: {str(e)}!!!'}, 500


def read_all_data(collection_name):
    """
    Read all the documents in the specified Firestore collection.

    Args:
        collection_name (str): The name of the Firestore collection.

    Returns:
        list: List of documents in the collection.
    """
    try:
        docs = db.collection(collection_name).stream()
        return docs
    except Exception as e:
        print('Error reading data:', e)
        raise e
