import logging
from dataclasses import dataclass

import openai

from util.message import Message


@dataclass
class OpenAIResponse:
    response: str
    tokens: int


def exchange(messages: list[Message]) -> OpenAIResponse:
    openai_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[message.as_dict() for message in messages]
    )
    tokens = openai_response["usage"]["total_tokens"]
    response = openai_response["choices"][0]["message"]["content"]
    logging.debug(f"Received response: {response}")
    return OpenAIResponse(response=response, tokens=tokens)
