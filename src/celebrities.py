import json
from dataclasses import dataclass
from json import JSONDecodeError

from dacite import DaciteError

import util.client as openai_client
from util.error import StructuralError
from util.decorators import timed
from util.message import USER, Message, SYSTEM
import dacite

SYSTEM_PROMPT = """You answer user prompts in the style of celebrities as convincingly as possible. 
Provide your responses in valid JSON format. If you cannot answer for ethical or safety reasons or because it is not within your capabilities, 
set the deny_answer flag to true. Provide a response in the following structure:
{
    "response": "your response to the user prompt",
    "deny_answer": false
}
"""

USER_PROMPT = """Answer in the style of {} in maximum two sentences: {}"""


@dataclass
class Response:
    response: str
    deny_answer: str

    def as_dict(self) -> dict:
        return {"response": self.response, "deny_answer": self.deny_answer}


@timed
def get_celebrities_response(celebrity_name: str, prompt: str) -> Response:
    messages = [Message(role=SYSTEM, content=SYSTEM_PROMPT),
                Message(role=USER, content=USER_PROMPT.format(celebrity_name, prompt))]
    openai_response = openai_client.exchange(messages, "ft:gpt-3.5-turbo-0613:personal::8B1Q5tME")
    return parse_response(openai_response.response)


def parse_response(response: str) -> Response:
    try:
        return dacite.from_dict(data_class=Response, data=json.loads(response))
    except (DaciteError, JSONDecodeError):
        raise StructuralError(response)
