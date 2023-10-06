import logging

import json5 as json
import openai

from diff import diff
from message import Message, SYSTEM, USER
from prompt import CHECKER_SYSTEM_PROMPT, CHECKER_USER_PROMPT


def check_email(email: str) -> dict:
    session = [Message(role=SYSTEM, content=CHECKER_SYSTEM_PROMPT),
               Message(role=USER, content=CHECKER_USER_PROMPT.format(email))]
    response = _openai_exchange(session)
    processed_response = post_process(response)
    logging.info(f"Processed suggestions: {processed_response}")
    return {"original_email": email, "suggestions": processed_response}


def _openai_exchange(messages: list[Message]) -> list[dict]:
    openai_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[message.as_dict() for message in messages]
    )
    response = openai_response["choices"][0]["message"]["content"]
    logging.debug(f"Received response: {response}")
    return parse_response(response)


def parse_response(gpt_response: str) -> list[dict]:
    return json.loads(gpt_response)


def post_process(suggestions: list[dict]) -> list[dict]:
    logging.info(f"Received suggestions: {suggestions}")
    return [{"sentence": suggestion["original_sentence"],
             "diff": diff(suggestion["original_sentence"], suggestion["improved_sentence"])}
            for suggestion in suggestions if suggestion["original_sentence"] != suggestion["improved_sentence"]]
