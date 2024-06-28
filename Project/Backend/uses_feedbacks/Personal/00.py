data = {'Records': [{'eventID': '2d31faec7f2d44b1f3ae5f16b4e9f6d9', 'eventName': 'REMOVE', 'eventVersion': '1.1', 'eventSource': 'aws:dynamodb', 'awsRegion': 'us-east-1', 'dynamodb': {'ApproximateCreationDateTime': 1719543861.0, 'Keys': {'feedback_id': {'S': '94c996d3-34f3-11ef-abeb-f5c0c47d5787'}}, 'OldImage': {'feedback': {'S': 'This is a test feedback 3...'}, 'date_time': {'S': '2025-09-05 12:33:25'}, 'feedback_id': {'S': '94c996d3-34f3-11ef-abeb-f5c0c47d5787'}, 'username': {'S': 'sam'}}, 'SequenceNumber': '1163700000000087377819209', 'SizeBytes': 169, 'StreamViewType': 'NEW_AND_OLD_IMAGES'}, 'eventSourceARN': 'arn:aws:dynamodb:us-east-1:921369520595:table/users_feedbacks_table/stream/2024-06-28T01:58:05.187'}]}


def main():
    if data['Records'][0]['dynamodb']['NewImage']:
        print("ase...")
    else:
        print("nai...")


if __name__ == '__main__':
    main()
