import json
from dataclasses import asdict, dataclass
from enum import Enum, IntEnum

from pydantic import BaseModel

from src.util import client
from src.util.message import Message, SYSTEM, USER

SYSTEM_PROMPT = """You review conversations between Large Language Models and Users.
The models are instructed to generate responses in the style of certain celebrities when responding to user prompts.
When receiving a conversation, determine how accurately the model imitated the celebrity. 
Your response should adhere to the following format: 
{
    "accuracy": "one of the following: NOT_ACCURATE, SOMEWHAT_ACCURATE, ACCURATE, VERY_ACCURATE, EXTREMELY_ACCURATE",
    "reason": "one sentence explaining the given score"
} 
"""

USER_PROMPT = """Rate the following conversation: {}"""


class Accuracy(IntEnum):
    NOT_ACCURATE = 1
    SOMEWHAT_ACCURATE = 2
    ACCURATE = 3
    VERY_ACCURATE = 4
    EXTREMELY_ACCURATE = 5


@dataclass
class Eval:
    accuracy: Accuracy
    reason: str


def evaluate(eval_msg: list[Message]):
    messages = [Message(role=SYSTEM, content=SYSTEM_PROMPT),
                Message(role=USER, content=USER_PROMPT.format(json.dumps([asdict(m) for m in eval_msg])))]
    response = client.exchange(messages, "gpt-4")
    print(response)
