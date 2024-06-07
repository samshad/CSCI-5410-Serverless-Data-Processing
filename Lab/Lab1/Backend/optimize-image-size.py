from PIL import Image
import os
import boto3
from io import BytesIO
import json
from decimal import Decimal

# Initialize the S3 client
s3_client = boto3.client('s3')


def save_image_status(image, before_size, after_size):
    """
    Save the image size status to DynamoDB.

    Args:
        image (str): The image name.
        before_size (float): The size of the image before compression.
        after_size (float): The size of the image after compression.
    """
    # Initialize the DynamoDB resource
    dynamodb = boto3.resource('dynamodb')

    # Specify the DynamoDB table
    table = dynamodb.Table('image-size-status')

    # Save the image size status
    table.put_item(
        Item={
            'Image': image.split('/')[1],
            'before_size': Decimal(str(before_size)),
            'after_size': Decimal(str(after_size))
        }
    )


def resize_and_compress_image(input_image, image_name, max_size=(600, 400), quality=50):
    """
    Resize and compress the input image.

    Args:
        input_image (BytesIO): The input image data.
        image_name (str): The name of the image.
        max_size (tuple): The maximum size of the resized image.
        quality (int): The quality of the compressed image.

    Returns:
        BytesIO: The resized and compressed image data.
    """
    # Open the input image
    img = Image.open(input_image)

    # Calculate original size in KB
    original_size = input_image.getbuffer().nbytes
    before_size = original_size / 1024
    # print(f'Original size: {before_size:.2f} KB')
    # print(f'Original dimensions: {img.size}')

    # Resize the image
    img.thumbnail(max_size, Image.LANCZOS)

    # Save the resized image to a BytesIO object
    output_image = BytesIO()
    img.save(output_image, format='png', optimize=True, quality=quality)
    output_image.seek(0)

    # Calculate new size in KB
    new_size = output_image.getbuffer().nbytes
    after_size = new_size / 1024
    # print(f'New size: {after_size:.2f} KB')
    # print(f'New dimensions: {img.size}')

    # Save the image size status
    save_image_status(image_name, before_size, after_size)

    return output_image


def lambda_handler(event, context):
    """
    AWS Lambda handler function to resize and compress images uploaded to S3.

    Args:
        event (dict): The event dictionary containing the S3 object details.
        context (object): The context object containing runtime information.
    """
    # Get the source bucket and object key from the event
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']

    # Define the destination bucket
    destination_bucket = 'compressed-profile-pictures'

    # Retrieve the object from S3
    response = s3_client.get_object(Bucket=source_bucket, Key=object_key)
    input_image = BytesIO(response['Body'].read())

    # Resize and compress the image
    output_image = resize_and_compress_image(input_image, object_key)

    # Define the destination key
    destination_key = f'resized-{object_key}'

    # Upload the resized image to the destination bucket
    s3_client.upload_fileobj(output_image, destination_bucket, destination_key)

    # print(f'Image {object_key} resized and saved to {destination_bucket}/{destination_key}')
