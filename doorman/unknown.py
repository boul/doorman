import json
import boto3
import requests
import hashlib
import os
from urllib.parse import parse_qs

bucket_name = os.environ['BUCKET_NAME']
slack_token = os.environ['SLACK_API_TOKEN']
slack_channel_id = os.environ['SLACK_CHANNEL_ID']
slack_training_channel_id = os.environ['SLACK_TRAINING_CHANNEL_ID']
rekognition_collection_id = os.environ['REKOGNITION_COLLECTION_ID']


def unknown(event, context):
    try:
        print(event)
        key = event['Records'][0]['s3']['object']['key']
        print(key)
        
        data = {
            "channel": slack_training_channel_id,
            "text": "Unrecognized person, do you want me to recognize this person?",
            "attachments": [
                {
                    "image_url": "https://%s.s3.amazonaws.com/%s" % (bucket_name, key),
                    "fallback": "Nope?",
                    "callback_id": key,
                    "attachment_type": "default",
                    #  "actions": [{
                    #         "name": "username",
                    #         "text": "Select a username...",
                    #         "type": "select",
                    #         "data_source": "users",
                    #         "value": "new-user"
                    #     },
                    "actions": [
                        {
                            "name": "register",
                            "text": "Yes, use this picture!",
                            "type": "button",
                            "value": "register"
                        },
                        {
                            "name": "discard",
                            "text": "No! Delete Picture!",
                            "style": "danger",
                            "type": "button",
                            "value": "ignore",
                            "confirm": {
                                "title": "Are you sure?",
                                "text": "Are you sure you want to ignore and delete this image?",
                                "ok_text": "Yes",
                                "dismiss_text": "No"
                            }
                        }
                    ]
                }
            ]
        }
        print(data)
        foo = requests.post("https://slack.com/api/chat.postMessage", headers={'Content-Type':'application/json;charset=UTF-8', 'Authorization': 'Bearer %s' % slack_token}, json=data)
    
        print(foo.json())
        
    except Exception as ex:
        print("unknown.py encountered an error")
        print(ex)