import boto3
import os

session = boto3.session.Session(
    aws_access_key_id="",
    aws_secret_access_key="",
    aws_session_token=""
)


def lambda_handler(event, context):
    # Prepare the DynamoDB client
    dynamodb = session.resource("dynamodb")
    table_name = "image-size-status"
    table = dynamodb.Table(table_name)

    result = table.get_item(Key={"Image": event["user"]})["Item"]
    before_size: str = str(f"{result["before_size"]:.2f} KB")
    after_size: str = str(f"{result["after_size"]:.2f} KB")
    print(result["Image"], before_size, after_size)
    response = {"image_status": (result["Image"], before_size, after_size)}

    """response = table.get_item(Key={"user": user})

    if "Item" in response:
        visit_count = response["Item"]["visit_count"]

    attr = {
        "first": "Janae",
        "middle": "Elliott",
        "last": "Boyle"
      }

    # Get the visit count from the DynamoDB table
    response = table.get_item(Key={"user": user})
    if "Item" in response:
        visit_count = response["Item"]["visit_count"]

    # Increment the visit count and put the item into DynamoDB table.
    visit_count += 1
    table.put_item(Item={"user": user, "visit_count": visit_count})

    message: str = f"Hello {user}! You have visited us {visit_count} times."""
    return response


if __name__ == "__main__":
    os.environ["TABLE_NAME"] = "samtest"
    test_event = {"user": "asdf.jpg"}
    result = lambda_handler(test_event, None)
    print(result)
