from devtrac.main.tests.test_base import TestBase


class SubmissionTest(TestBase):
    def test_submission_model(self):
        self._add_submission()
