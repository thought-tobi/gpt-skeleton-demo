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


@app.route('/check', methods=['OPTIONS'])
def login():
    return jsonify({"msg": "all good!"}), 200


@app.route('/check', methods=['POST'])
def check_email():
    return jsonify({
        "original_email": "Hey Baywatch!\n\nAs you may know, the Hamburg office is pretty quiet these days. So, a few of us were thinking that it might be a good idea to organize a retrospective for the social events of the past few months. This would help us understand what people would like to see differently in the future. We're also considering using a Mural or a Questionnaire to gather feedback on what people might want from our upcoming events.\n\nThe format for this retrospective isn't quite clear at the moment. That's why I'm reaching out to see if there's anyone at the beach with experience in facilitating such discussions or designing cool Mural boards. Could you maybe help us out with this? Anything is appreciated. Thanks!\n\nKind regards,\n\nTobi",
        "suggestions": [
            {
                "diff": [
                    "- Hey",
                    "+ Hello",
                    "Baywatch!"
                ],
                "sentence": "Hey Baywatch!"
            },
            {
                "diff": [
                    "As",
                    "you",
                    "may",
                    "know,",
                    "the",
                    "Hamburg",
                    "office",
                    "is",
                    "- pretty",
                    "+ currently",
                    "+ quite",
                    "- quiet",
                    "+ quiet.",
                    "- these",
                    "- days."
                ],
                "sentence": "As you may know, the Hamburg office is pretty quiet these days."
            },
            {
                "diff": [
                    "+ A",
                    "- So,",
                    "- a",
                    "few",
                    "of",
                    "us",
                    "were",
                    "thinking",
                    "- that",
                    "it",
                    "might",
                    "be",
                    "a",
                    "good",
                    "idea",
                    "to",
                    "organize",
                    "a",
                    "retrospective",
                    "for",
                    "the",
                    "social",
                    "events",
                    "of",
                    "the",
                    "past",
                    "few",
                    "months."
                ],
                "sentence": "So, a few of us were thinking that it might be a good idea to organize a retrospective for the social events of the past few months."
            },
            {
                "diff": [
                    "This",
                    "would",
                    "help",
                    "us",
                    "understand",
                    "what",
                    "people",
                    "would",
                    "like",
                    "to",
                    "see",
                    "+ done",
                    "differently",
                    "in",
                    "the",
                    "future."
                ],
                "sentence": "This would help us understand what people would like to see differently in the future."
            },
            {
                "diff": [
                    "We're",
                    "also",
                    "considering",
                    "using",
                    "a",
                    "Mural",
                    "or",
                    "a",
                    "- Questionnaire",
                    "+ questionnaire",
                    "to",
                    "gather",
                    "feedback",
                    "on",
                    "what",
                    "people",
                    "might",
                    "want",
                    "from",
                    "our",
                    "upcoming",
                    "events."
                ],
                "sentence": "We're also considering using a Mural or a Questionnaire to gather feedback on what people might want from our upcoming events."
            },
            {
                "diff": [
                    "The",
                    "format",
                    "for",
                    "this",
                    "retrospective",
                    "- isn't",
                    "+ is",
                    "+ not",
                    "quite",
                    "clear",
                    "at",
                    "the",
                    "moment."
                ],
                "sentence": "The format for this retrospective isn't quite clear at the moment."
            },
            {
                "diff": [
                    "That's",
                    "why",
                    "I'm",
                    "reaching",
                    "out",
                    "to",
                    "see",
                    "if",
                    "- there's",
                    "+ there",
                    "+ is",
                    "anyone",
                    "at",
                    "the",
                    "beach",
                    "with",
                    "experience",
                    "in",
                    "facilitating",
                    "such",
                    "discussions",
                    "or",
                    "designing",
                    "cool",
                    "Mural",
                    "boards."
                ],
                "sentence": "That's why I'm reaching out to see if there's anyone at the beach with experience in facilitating such discussions or designing cool Mural boards."
            },
            {
                "diff": [
                    "- Could",
                    "+ Would",
                    "you",
                    "- maybe",
                    "+ be",
                    "+ able",
                    "+ to",
                    "help",
                    "us",
                    "out",
                    "with",
                    "this?"
                ],
                "sentence": "Could you maybe help us out with this?"
            },
            {
                "diff": [
                    "- Anything",
                    "- is",
                    "+ Any",
                    "+ assistance",
                    "+ would",
                    "+ be",
                    "+ greatly",
                    "appreciated."
                ],
                "sentence": "Anything is appreciated."
            }
        ]
    }), 200
