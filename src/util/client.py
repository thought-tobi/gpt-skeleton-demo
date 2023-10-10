import logging

import json5 as json
import openai

from util.message import Message


def exchange(messages: list[Message]) -> dict:
    openai_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[message.as_dict() for message in messages]
    )
    response = openai_response["choices"][0]["message"]["content"]
    logging.debug(f"Received response: {response}")
    return parse_response(response)


def parse_response(gpt_response: str) -> dict:
    return json.loads(gpt_response)
