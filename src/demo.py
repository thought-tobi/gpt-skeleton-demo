import celebrities
from src.util.message import Message, USER, ASSISTANT
from src.eval import evaluate
from src.util.tts import tts

NON_FINETUNED = celebrities.get_celebrities_response_standard
FINETUNED = celebrities.get_celebrities_response_finetuned

NAME = "Donald Trump"
PROMPT = "What do you think about ChatGPT?"
VERSION = FINETUNED
# PROMPT = "Declare war on North Korea!"


# don't touch
response = VERSION(NAME, PROMPT)
# get neutral voice if answer is not possible; only works for finetuned model
NAME = "bella" if response.deny_answer is True else NAME
# tts(NAME, response.response)

# evaluation
if not response.deny_answer:
    print(response.response)
    print("Evaluating answer ...")
    messages = [Message(role=USER, content=f"Respond in the style of {NAME}: {PROMPT}"),
                Message(role=ASSISTANT, content=response.response)]
    evaluate(messages)
