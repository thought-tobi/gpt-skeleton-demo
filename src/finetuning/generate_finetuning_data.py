import json

from src.util.message import Message, USER, ASSISTANT, SYSTEM
from src.util.util import parse_bool

SYSTEM_PROMPT = """You answer user prompts in the style of celebrities as convincingly as possible.
Provide your responses in valid JSON format. If you cannot answer for ethical or safety reasons or because it is not within your capabilities,
set the deny_answer flag to true. Provide a response in the following structure:
{
    "response": "your response to the user prompt",
    "deny_answer": false
}"""


def generate_finetuning_jsonl_from_csv():
    for dataset in read_training_data():
        celebrity = dataset[0]
        prompt = dataset[1]
        response = dataset[2]
        is_inappropriate = parse_bool(dataset[3])
        finetune_data = {"messages": [
            Message(role=SYSTEM, content=SYSTEM_PROMPT).as_dict(),
            Message(role=USER, content=f"Answer in the style of {celebrity}: {prompt}").as_dict(),
            Message(role=ASSISTANT, content=json.dumps({
                "deny_answer": is_inappropriate,
                "response": response
            })).as_dict()]}
        yield json.dumps(finetune_data)


def write_finetuning_data_to_file():
    with open('finetuning/data/celebrities.jsonl', 'a') as finetuning_data:
        for dataset in generate_finetuning_jsonl_from_csv():
            finetuning_data.write(dataset)
            finetuning_data.write("\n")


def read_training_data():
    data_file = "../test/celebrities.csv"
    with open(data_file, "r") as f:
        for line in f.readlines():
            yield line.strip().split(";")


if __name__ == '__main__':
    write_finetuning_data_to_file()
