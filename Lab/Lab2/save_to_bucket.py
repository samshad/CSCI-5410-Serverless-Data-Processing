from cloudevents.http import CloudEvent
import functions_framework
from google.events.cloud import firestore
from google.cloud import storage
import requests
import pandas as pd

from Personal.urls import GET_FEEDBACKS_URL, BUCKET_NAME


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

    # Save all feedbacks to a Google Cloud Storage bucket as a CSV file
    save_to_bucket()


def get_feedbacks():
    """
    Retrieve all feedbacks from the database.

    Returns:
        list: List of feedbacks retrieved from the database.
    """
    url = GET_FEEDBACKS_URL

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()['feedbacks']


def save_to_bucket():
    """
    Save all feedbacks to a Google Cloud Storage bucket as a CSV file.

    Returns:
        None
    """
    feedbacks = get_feedbacks()

    # Convert feedbacks to a DataFrame
    df = pd.DataFrame(feedbacks)[['username', 'feedback', 'score', 'polarity']]

    # Initialize the Google Cloud Storage client
    storage_client = storage.Client()

    # Get the bucket
    bucket = storage_client.bucket(BUCKET_NAME)

    # Save the DataFrame to the bucket as a CSV file
    bucket.blob('feedbacks.csv').upload_from_string(df.to_csv(index=False), 'text/csv')
