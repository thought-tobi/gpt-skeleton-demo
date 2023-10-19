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
    return openai.FineTuningJob.create(training_file="file-DATNhZ6Odm3jGpTih6Zl0scM", model="gpt-3.5-turbo")


def list_files():
    print(openai.File.list())


def get_jobs():
    print(openai.FineTuningJob.list())


if __name__ == '__main__':
    get_jobs()
