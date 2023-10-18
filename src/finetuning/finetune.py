import os
from dotenv import load_dotenv
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def create_file():
    return openai.File.create(
        file=open("data/celebrities.jsonl", "rb"),
        purpose='fine-tune'
    )


def perform_finetuning():
    openai.FineTuningJob.create(training_file="file-R8XqL9HJzcuP90YUscmECFJX", model="gpt-3.5-turbo")


def list_files():
    print(openai.File.list())


def get_jobs():
    print(openai.FineTuningJob.list())


if __name__ == '__main__':
    get_jobs()
