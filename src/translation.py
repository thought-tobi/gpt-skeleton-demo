import concurrent
import json
from dataclasses import dataclass, field
from json import JSONDecodeError

import dacite
from dacite import DaciteError

from src.util.decorators import timed
from src.util.error import StructuralError
from src.util.message import Message, USER
from util.client import exchange

SYSTEM_PROMPT = """Translate the following sentence into English and identify the source language.
Provide the response in the following structure:
{
  "translation": "a translation of the source sentence",
  "language": "the source language of the sentence"
}

Sentence: 
"""


@dataclass
class Translation:
    translation: str
    language: str


@timed
def get_translation_and_source_language(sentence: str) -> Translation:
    messages = [Message(role=USER, content=SYSTEM_PROMPT + sentence)]
    response = exchange(messages)
    return parse_response(response)


def parse_response(response: str) -> Translation:
    try:
        return dacite.from_dict(data_class=Translation, data=json.loads(response))
    except (DaciteError, JSONDecodeError):
        raise StructuralError(response)
