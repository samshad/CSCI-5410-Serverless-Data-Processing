from cloudevents.http import CloudEvent
import functions_framework
from google.events.cloud import firestore
import json
import requests

from Personal.urls import SENTIMENT_POST_URL, INSERT_DATA_URL


@functions_framework.cloud_event
def hello_firestore(cloud_event: CloudEvent) -> None:
    """
    Cloud Function triggered by a change to a Firestore document.
    Extracts data from the Firestore document change event, performs sentiment analysis,
    and inserts the analyzed data into another database.

    Args:
        cloud_event (CloudEvent): Cloud event with information on the Firestore event trigger.
    """
    # Parse the Firestore event payload
    firestore_payload = firestore.DocumentEventData()
    firestore_payload._pb.ParseFromString(cloud_event.data)

    print(f"Function triggered by change to: {cloud_event['source']}")

    # Extract necessary fields from the Firestore event payload
    username = firestore_payload.value.fields['username'].string_value
    feedback = firestore_payload.value.fields['feedback'].string_value

    # Perform sentiment analysis on the feedback
    sentiment = get_sentiment(feedback)
    score = sentiment['score']
    polarity = sentiment['polarity']

    # Prepare data to be inserted into the new collection
    data_to_insert = {
        'username': username,
        'feedback': feedback,
        'score': score,
        'polarity': polarity
    }

    # Insert the analyzed data into another database
    response = insert_data(data_to_insert)
    print("INSERT response:", response)


def get_sentiment(feedback):
    """
    Perform sentiment analysis on the provided feedback text.

    Args:
        feedback (str): The feedback text to analyze.

    Returns:
        dict: The sentiment analysis result containing score and polarity.
    """
    url = SENTIMENT_POST_URL

    payload = json.dumps({"text": feedback})
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, headers=headers, data=payload)
    return response.json()


def insert_data(data):
    """
    Insert the analyzed data into another database.

    Args:
        data (dict): The data to insert.

    Returns:
        tuple: Response message and status code from the insertion request.
    """
    url = INSERT_DATA_URL

    payload = json.dumps(data)
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, headers=headers, data=payload)
    return {'message': response.text}, response.status_code
