import os
import requests
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/', methods=['POST'])
@app.route('/api/detect', methods=['POST'])
def proxy_detect():
    api_url = os.environ.get('DETECTION_API_URL')
    if not api_url:
        return {"error": "DETECTION_API_URL not configured in Vercel ENV settings"}, 500

    # Forward the file and other form data
    files = {
        'file': (request.files['file'].filename, request.files['file'].read(), request.files['file'].content_type)
    }
    
    try:
        response = requests.post(api_url, files=files)
        return Response(response.content, status=response.status_code, content_type=response.headers['content-type'])
    except Exception as e:
        return {"error": str(e)}, 500
