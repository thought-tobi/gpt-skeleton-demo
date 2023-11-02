import logging
import os

import openai
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from celebrities import get_celebrities_response_finetuned
from translation import get_translation_and_source_language

# setup
load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

# configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

app = Flask(__name__)
CORS(app)


@app.route('/celebrities', methods=['POST'])
def get_celebrity_response():
    celebrity_name = request.json['celebrity_name']
    prompt = request.json['prompt']
    logging.info(f"Getting response for prompt {prompt} in the style of {celebrity_name} ...")
    return jsonify(get_celebrities_response_finetuned(celebrity_name, prompt).as_dict()), 200


@app.route('/translation', methods=['POST'])
def get_translation():
    sentence = request.json['sentence']
    logging.info(f"Getting translation for sentence '{sentence}'")
    return jsonify(get_translation_and_source_language(sentence)), 200
