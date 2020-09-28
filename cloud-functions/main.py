from google.cloud import pubsub_v1 as pubsub
import time
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'key.json'
proj_name = 'distcomp-project-1'
sub_name = 'my-sub'


def callback(message):
    print('Received message: {}'.format(message.data.decode("utf-8")))
    if message.attributes:
        print('Attributes:')
        for key in message.attributes:
            value = message.attributes.get(key)
            print('{}: {}'.format(key, value))
    message.ack()


def sub_pull():
    subscriber = pubsub.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        proj_name, sub_name)
    subscriber.subscribe(subscription_path, callback=callback)
    print('Listening for messages on: {}'.format(subscription_path))
    while True:
        time.sleep(30)


if __name__ == "__main__":
    sub_pull()




from google.cloud import storage
import google

def create_bucket_class_location(bucket_name):
    """Create a new bucket in specific location with storage class"""
    # bucket_name = "your-new-bucket-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = "COLDLINE"
    new_bucket = storage_client.create_bucket(bucket, location="us")

    print(
        "Created bucket {} in {} with storage class {}".format(
            new_bucket.name, new_bucket.location, new_bucket.storage_class
        )
    )
    return new_bucket




