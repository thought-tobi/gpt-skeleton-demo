import logging
import os
from unittest import TestCase

import client

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def read_test_data() -> list:
    test_dir = "../test"
    # read all files in test directory
    # return list of base64 encoded strings
    for file in os.listdir(test_dir):
        with open(f"{test_dir}/{file}", "r") as f:
            yield f.read()


class TestBenchmark(TestCase):

    errors = {
        "structural_errors": 0,
        "content_errors": 0,
    }

    def test_benchmark(self):
        test_data = list(read_test_data())
        for email in test_data:
            logging.info(f"Testing email: {email}")
            response = client.check_email(email)
            logging.info(f"Received response: {response}")

            # verify structure
            self.assertIn("original_email", response)
            self.assertIn("suggestions", response)

            # verify suggestions
            suggestions = response["suggestions"]
            self.assertIsInstance(suggestions, list)
            for suggestion in suggestions:
                self.assertIn("original_sentence", suggestion)
                self.assertIn("improved_sentence", suggestion)

                # verify that sentences are not identical, primarily to save tokens
                if suggestion["original_sentence"] == suggestion["improved_sentence"]:
                    logging.warning(f"Original sentence and improved sentence are the same: {suggestion}")
                    self.errors["content_errors"] = self.errors["content_errors"] + 1

                # verify that original sentence is in email to prevent hallucinations
                if suggestion["original_sentence"] not in email:
                    logging.warning(f"Original sentence not in email: {suggestion}")
                    self.errors["content_errors"] = self.errors["content_errors"] + 1

        self.assertLessEqual(self.errors["content_errors"], 2)

