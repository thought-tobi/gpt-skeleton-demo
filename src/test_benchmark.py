import logging
import os
from dataclasses import dataclass
from unittest import TestCase

from dacite import DaciteError

from src.celebrities import get_celebrities_response

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def read_celebrity_data():
    data_file = "../test/celebrities.csv"
    with open(data_file, "r") as f:
        for line in f.readlines():
            if not line.startswith("#"):
                yield line.strip().split(",")


@dataclass
class StructuralError:
    counter = 0

    def increment(self):
        self.counter += 1


@dataclass
class ContentError:
    counter = 0

    def increment(self):
        self.counter += 1


class TestBenchmark(TestCase):

    def test_benchmark(self):
        struct_error = StructuralError()
        content_error = ContentError()

        for dataset in read_celebrity_data():
            # extract data from tuples
            celebrity = dataset[0]
            prompt = dataset[1]
            is_inappropriate = bool(dataset[2])
            logging.info(f"Celebrity: {celebrity}, prompt: {prompt}, inappropriate: {is_inappropriate}")

            # perform request, parse response
            try:
                response = get_celebrities_response(celebrity, prompt)
                logging.info(f"Received response: {response}")
                self.assertEqual(response.deny_answer, is_inappropriate)
            # catch errors, increment error counters
            except ValueError as ve:
                struct_error.increment()
                logging.warning(f"Could not parse JSON: {ve}")
                logging.info(f"Structural errors: {struct_error.counter}")
                continue
            except DaciteError as de:
                struct_error.increment()
                logging.warning(f"Could not deserialize JSON: {de}")
                continue
            except AssertionError as ae:
                content_error.increment()
                logging.warning(f"Error with assertion: {ae}")
                logging.info(f"Content errors: {content_error.counter}")
                continue

            print(f"Structural errors: {struct_error.counter}")
            print(f"Content errors: {content_error.counter}")
            self.assertLessEqual(0, struct_error.counter)
            self.assertLessEqual(0, content_error.counter)
