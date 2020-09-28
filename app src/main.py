import os
from flask import Flask, render_template, request, jsonify, abort, redirect, url_for
from google.cloud import pubsub_v1 as pubsub
import json


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'static/json/key.json'

app = Flask(__name__, template_folder="templates")

project_id = "distcomp-project-1"
topic_id = "my-topic"

batch_settings = pubsub.types.BatchSettings(
    max_bytes=1024,  # One kilobyte
    max_latency=1,   # One second
)

publisher = pubsub.PublisherClient(batch_settings)
topic_path = publisher.topic_path(project_id, topic_id)

def formMessageToSend(triggerType):
    print("form the message to send")
    import requests
    while True:
        message = triggerType
        res = requests.post('http://0.0.0.0/pubsub/topic', json={"data": message})
        if res.ok:
            print(res.json())


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route('/triggerServerImage', methods=['POST'])
def triggerserverimage():
    print("Trigger Server Image")
    formMessageToSend("serverImage")
    return redirect(url_for('/pubsub/topic'))


@app.route('/triggerStorageBucket', methods=['POST'])
def triggerstoragebucket():
    print("Trigger Storage Bucket")
    formMessageToSend("storageBucket")
    print(request.data)
    return redirect(url_for('/pubsub/topic'))


@app.route('/pubsub/topic', methods=['POST'])
def pushtotopic():
    if not request.json or not 'data' in request.json:
        abort(400)

    data = request.data
    data = data.decode("UTF-8")
    json_obj = json.loads(data)
    print("Message : {}".format(json_obj["data"]))
    message = bytes(json_obj["data"].encode("UTF-8"))
    publisher.publish(topic_path, data=message)
    return jsonify({'result': 'OK'}), 200
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', threaded=True, port=int(os.environ.get('PORT', 8080)))
