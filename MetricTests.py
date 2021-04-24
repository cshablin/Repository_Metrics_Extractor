import os
import unittest

from git import Repo

from RepoMetricExtractor import get_commit_2_methods_metric_2, MetricExtractor


class MyTestCase(unittest.TestCase):

    repo_path = "C:\\temp\\tmp_repo"

    def test_repo_checkout_commit(self):
        repo_url = "https://github.com/apache/maven.git"
        extractor = MetricExtractor(repo_url, self.repo_path)
        repo = Repo(self.repo_path)
        self.assertTrue(not repo.bare)
        commit_id = "778f044e"
        extractor.checkout(commit_id)
        commit = repo.head.commit
        self.assertTrue(commit_id in str(commit))
        extractor.remove_repo()

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == '__main__':
    unittest.main()
