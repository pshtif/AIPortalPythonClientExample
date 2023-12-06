# Created by Peter @sHTiF Stefcek
# 
# Example python script to communicate with AI Portal

import requests
import json
from requests import Request, Session
from requests_toolbelt.multipart.encoder import MultipartEncoder

# Request image generation from the AI server

url = 'http://localhost/image/generate'

multipart_data = MultipartEncoder(
    fields={
        'prompt': 'bear on a desert',
        'image_width': '1024',
        'image_height': '1024',
        'negative_prompt': '',
        'model': '',
        'image_count': '1',
        'steps': '20',
        'cfg': '7.5',
        'lora': 'none',
        'lora_weight': '0.5',
        'strength': '0.75',
        'conditioning_scale': '0.8',
        'conditioning_factor': '0.8',
        'seed': '0',
        'background': 'False',
        # 'image_source_blob': ('filename', open('path_to_file', 'rb'), 'image/jpeg'),
        'image_source_type': 'none',
    }
)

session = Session()
request = Request('POST', url, data=multipart_data, headers={'Content-Type': multipart_data.content_type})
prepared_request = session.prepare_request(request)

response = session.send(prepared_request)
print(response.status_code)

if response.status_code == 200:
    print("Request successful!")
    print(response.json())
    request_id = response.json()['request_id']
else:
    print("Request failed.")
    print(response.json())


# CHECK PROGRESS

url = 'http://localhost/image/get_progress'


params = {
    'request_id': request_id,
}


response = requests.get(url, params=params, stream=True)


if response.status_code == 200:
    print("Streaming response started...")
    try:
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith('data:'):
                    data = json.loads(decoded_line.split(":", 1)[1].strip())
                    print(data)

                    # Break the loop if completed
                    if data.get("completed", False):
                        print("Progress complete.")
                        break
    except KeyboardInterrupt:
        print("Streaming stopped by user.")
else:
    print("Request failed.")
    print(response.text)