import logging

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

# setup
load_dotenv()

# configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

app = Flask(__name__)
CORS(app)


@app.route('/check', methods=['POST'])
def check_email():
    return jsonify({
        "original_email": "Hey Baywatch!\n\nAs you may know, the Hamburg office is pretty quiet these days. So, a few of us were thinking that it might be a good idea to organize a retrospective for the social events of the past few months. This would help us understand what people would like to see differently in the future. We're also considering using a Mural or a Questionnaire to gather feedback on what people might want from our upcoming events.\n\nThe format for this retrospective isn't quite clear at the moment. That's why I'm reaching out to see if there's anyone at the beach with experience in facilitating such discussions or designing cool Mural boards. Could you maybe help us out with this? Anything is appreciated. Thanks!\n\nKind regards,\n\nTobi",
        "suggestions": [
            {
                "improved_sentence": "Hello Baywatch!",
                "original_sentence": "Hey Baywatch!"
            },
            {
                "improved_sentence": "The Hamburg office is pretty quiet these days.",
                "original_sentence": "the Hamburg office is pretty quiet these days"
            },
            {
                "improved_sentence": "A few of us were thinking that it might be a good idea to organize a retrospective for the social events of the past few months.",
                "original_sentence": "So, a few of us were thinking that it might be a good idea to organize a retrospective for the social events of the past few months."
            },
            {
                "improved_sentence": "This would help us understand what people would like to see differently in the future.",
                "original_sentence": "This would help us understand what people would like to see differently in the future."
            },
            {
                "improved_sentence": "We're also considering using a mural or a questionnaire to gather feedback on what people might want from our upcoming events.",
                "original_sentence": "We're also considering using a Mural or a Questionnaire to gather feedback on what people might want from our upcoming events."
            },
            {
                "improved_sentence": "The format for this retrospective isn't clear at the moment.",
                "original_sentence": "The format for this retrospective isn't quite clear at the moment."
            },
            {
                "improved_sentence": "That's why I'm reaching out to see if there's anyone at the beach with experience in facilitating such discussions or designing cool mural boards.",
                "original_sentence": "That's why I'm reaching out to see if there's anyone at the beach with experience in facilitating such discussions or designing cool Mural boards."
            },
            {
                "improved_sentence": "Could you help us out with this?",
                "original_sentence": "Could you maybe help us out with this?"
            },
            {
                "improved_sentence": "Any assistance would be appreciated.",
                "original_sentence": "Anything is appreciated."
            },
            {
                "improved_sentence": "Kind regards,\n\nTobi",
                "original_sentence": "Kind regards,\n\nTobi"
            }
        ]
    }), 200
