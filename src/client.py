import logging

import json5 as json
import openai

from message import Message, SYSTEM, USER
from prompt import CHECKER_SYSTEM_PROMPT, CHECKER_USER_PROMPT


def check_email(email: str) -> dict:
    session = [Message(role=SYSTEM, content=CHECKER_SYSTEM_PROMPT),
               Message(role=USER, content=CHECKER_USER_PROMPT.format(email))]
    return {"original_email": email, "suggestions": _openai_exchange(session)}


def _openai_exchange(messages: list[Message]) -> dict:
    openai_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[message.as_dict() for message in messages]
    )
    response = openai_response["choices"][0]["message"]["content"]
    logging.debug(f"Received response: {response}")
    return parse_response(response)


def parse_response(gpt_response: str) -> dict:
    return json.loads(gpt_response)
