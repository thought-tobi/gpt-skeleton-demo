import base64
import logging
import os

import openai
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

import client

# setup
load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

# configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

app = Flask(__name__)
CORS(app)


@app.route('/check', methods=['POST'])
def check_email():
    email = request.stream.read()
    logging.info(f"Received sentence: {email}")
    if not email:
        return jsonify({'error': 'No email provided'}), 400
    email = base64.b64decode(email).decode('utf-8')
    logging.info(f"Decoded email: {email}")
    return client.check_email(email)
