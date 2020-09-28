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
