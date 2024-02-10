from unittest import TestCase

from app.agents.pull import PullAgent


class TestPullAgent(TestCase):
    def test_run(self):
        model = PullAgent()
        model.run_formulating(
            data_specification_request="Give a short name to the data you just uploaded"
        )


class TestPullAgent(TestCase):
    def test_is_run_classifying_ok(self):
        PullAgent().is_run_classifying_ok("Test")
