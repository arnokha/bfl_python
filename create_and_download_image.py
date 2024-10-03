import os
import requests
import time

BFL_API_KEY = "" or os.environ.get("BFL_API_KEY") 
if not BFL_API_KEY:
    raise ValueError("Must provide black forest labs API key via export (or insert value directly into script for BFL_API_KEY if you are not commiting or sharing this code)")

PROMPT = ""
IMG_WIDTH = 0
IMG_HEIGHT = 0

## TODO get prompt, width, and height via command line args. 
## it's ok for the user to modify script vals instead, but it must be provided somewhere
## if no valid value for any of these, throw an error and print usage string
## END TODO


request = requests.post(
    'https://api.bfl.ml/v1/flux-pro-1.1',
    headers={
        'accept': 'application/json',
        'x-key': BFL_API_KEY,
        'Content-Type': 'application/json',
    },
    json={
        'prompt': PROMPT,
        'width': IMG_WIDTH,
        'height': IMG_HEIGHT,
    },
).json()

print(request) ## TODO print only relevant parts and make sure nicely formatted

request_id = request["id"]

## TODO - this is copied from the API docs, but it's not clear how to save the resulting image to a file. Probably need to run this once to test.
while True:
    time.sleep(0.5)
    result = requests.get(
        'https://api.bfl.ml/v1/get_result',
        headers={
            'accept': 'application/json',
            'x-key': BFL_API_KEY,
        },
        params={
            'id': request_id,
        },
    ).json()
    if result["status"] == "Ready":
        print(f"Result: {result['result']['sample']}")
        break
    else:
        print(f"Status: {result['status']}")
