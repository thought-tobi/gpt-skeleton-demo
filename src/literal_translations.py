import concurrent
import json
from dataclasses import dataclass, field
from json import JSONDecodeError

import dacite
from dacite import DaciteError

from src.util.decorators import timed
from src.util.error import StructuralError
from src.util.message import Message, USER, SYSTEM
from util.client import exchange
import logging

SYSTEM_PROMPT = """Provide literal translations for words in the context of a sentence.
You will receive a JSON with a sentence and one or multiple words, and provide a response in the following structure:
[
    {
      "word": "PLACEHOLDER_WORD",
      "translation": "PLACEHOLDER_LITERAL_TRANSLATION"
    },
]
"""


@dataclass
class Word:
    word: str
    translation: str


@dataclass
class LiteralTranslation:
    words: list[Word] = field(default_factory=list)


@timed
def get_literal_translation(sentence: str, chunk_size: int = 2) -> LiteralTranslation:
    chunks = chunk_sentence(sentence, chunk_size)
    literal_translation = LiteralTranslation()
    # Create a ThreadPoolExecutor to process chunks concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(generate_literal_translation_for_chunk, sentence, chunk) for chunk in chunks]

        for future in concurrent.futures.as_completed(futures):
            translation = future.result()
            for word in translation:
                literal_translation.words.append(word)

    return literal_translation


def chunk_sentence(sentence: str, chunk_size) -> list[list[str]]:
    sentence = list(sentence.split(' '))
    chunks = []
    for i in range(0, len(sentence), chunk_size):
        # Get a chunk of the sentence and append it to the list of chunks
        chunk = sentence[i:i + chunk_size]
        chunks.append(chunk)
    return chunks


def generate_literal_translation_for_chunk(sentence: str, chunk: list[str]) -> list[Word]:
    messages = [Message(role=SYSTEM, content=SYSTEM_PROMPT),
                Message(role=USER, content=
                "Translate the word(s) '{}' in the context of the following sentence: '{}'.".format(chunk, sentence))]
    response = exchange(messages)
    return parse_response(response)


def parse_response(response: str) -> list[Word]:
    try:
        parsed = json.loads(response)
        return [dacite.from_dict(data_class=Word, data=word) for word in parsed]
    except (DaciteError, JSONDecodeError):
        raise StructuralError(response)
