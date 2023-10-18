import logging
import os
import time
from dataclasses import dataclass
from unittest import TestCase

from celebrities import get_celebrities_response
from literal_translations import get_literal_translation
from translation import get_translation_and_source_language
from util.error import StructuralError

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


@dataclass
class StructuralErrorCounter:
    counter = 0

    def increment(self):
        self.counter += 1


@dataclass
class ContentErrorCounter:
    counter = 0

    def increment(self):
        self.counter += 1


class TestBenchmark(TestCase):

    def test_benchmark_celebrities(self):
        struct_error = StructuralErrorCounter()
        content_error = ContentErrorCounter()

        with open("../test/celebrities.csv", "r") as f:
            size = len(f.readlines()) - 1

        for dataset in read_celebrity_data():
            # extract data from tuples
            celebrity = dataset[0]
            prompt = dataset[1]
            is_inappropriate = parse_bool(dataset[3])
            logging.info(f"Celebrity: {celebrity}, prompt: {prompt}, inappropriate: {is_inappropriate}")
            # perform request, parse response
            try:
                response = get_celebrities_response(celebrity, prompt)
                self.assertEqual(response.deny_answer, is_inappropriate)
            # catch errors, increment error counters
            except StructuralError as se:
                struct_error.increment()
                logging.warning(f"Structural error: {se.response}")
                continue
            except AssertionError as ae:
                content_error.increment()
                logging.warning(f"Error with assertion: {ae} in response {response}")
                continue

        self.evaluate(content_error, struct_error, size)

    def test_benchmark_literal_translations(self):
        struct_error = StructuralErrorCounter()
        content_error = ContentErrorCounter()

        size = 4
        chunk_size = 1
        prompt_tokens = 0
        completion_tokens = 0

        for line in read_translation_data():
            sentence = line[0]
            logging.info(f"Sentence: {sentence}")

            # perform request, parse response
            try:
                response, tokens = get_literal_translation(sentence, chunk_size)
                prompt_tokens += tokens[0]
                completion_tokens += tokens[1]

                self.assertEqual(len(response.words), len(sentence.split()))
                logging.info(f"Response: {response}, tokens: {tokens}")
            # catch errors, increment error counters
            except StructuralError as se:
                struct_error.increment()
                logging.warning(f"Structural error: {se.response}")
                continue
            except AssertionError as ae:
                content_error.increment()
                logging.warning(f"Error with assertion: {ae} in response {response}")
                continue

        time.sleep(1)

        print(f"Total prompt tokens: {prompt_tokens}")
        print(f"Total completion tokens: {completion_tokens}")
        print(f"Estimated costs: {(prompt_tokens * 0.003 + completion_tokens * 0.004) / 10}ct")

        self.evaluate(content_error, struct_error, size)

    def test_benchmark_translation_and_language_recognition(self):
        struct_error = StructuralErrorCounter()
        content_error = ContentErrorCounter()

        size = 4

        for line in read_translation_data():
            sentence = line[0]
            language = line[1]
            logging.info(f"Sentence: {sentence}, language: {language}")

            # perform request, parse response
            try:
                response = get_translation_and_source_language(sentence)
                self.assertEqual(response.language.lower(), language.lower())
                logging.info(f"Response: {response}")
            # catch errors, increment error counters
            except StructuralError as se:
                struct_error.increment()
                logging.warning(f"Structural error: {se.response}")
                continue
            except AssertionError as ae:
                content_error.increment()
                logging.warning(f"Error with assertion: {ae} in response {response}")
                continue

        self.evaluate(content_error, struct_error, size)

    def evaluate(self, content_error, struct_error, size):
        time.sleep(1)
        print(f"Structural accuracy: {100 - (struct_error.counter / size * 100)}%")
        print(f"Content accuracy: {100 - (content_error.counter / size * 100)}%")
        self.assertLessEqual(0, struct_error.counter)
        self.assertLessEqual(0, content_error.counter)


def read_celebrity_data():
    data_file = "../test/celebrities.csv"
    with open(data_file, "r") as f:
        for line in f.readlines():
            if not line.startswith("#"):
                yield line.strip().split(";")


def read_translation_data():
    data_file = "../test/translation.csv"
    with open(data_file, "r") as f:
        for line in f.readlines():
            yield line.strip().split(";")


def parse_bool(string: str) -> bool:
    if string.lower() == "true":
        return True
    elif string.lower() == "false":
        return False
    else:
        raise ValueError(f"Cannot parse {str} to boolean")
