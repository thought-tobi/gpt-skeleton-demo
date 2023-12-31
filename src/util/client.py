import logging
from dataclasses import dataclass

import openai

from util.message import Message


@dataclass
class OpenAIResponse:
    response: str
    tokens: (int, int)


def exchange(messages: list[Message], model: str = "gpt-3.5-turbo") -> OpenAIResponse:
    openai_response = openai.ChatCompletion.create(
        model=model,
        messages=[message.as_dict() for message in messages],
    )
    tokens = (openai_response["usage"]["prompt_tokens"], openai_response["usage"]["completion_tokens"])
    response = openai_response["choices"][0]["message"]["content"]
    logging.info(f"Received response: {response}, {tokens} tokens")
    return OpenAIResponse(response=response, tokens=tokens)
