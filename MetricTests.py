import unittest

from git import Repo

from RepoMetricExtractor import get_commit_2_methods_metric_2, MetricExtractor


class MyTestCase(unittest.TestCase):

    # def test_repo_loading(self):
    #     repo_path = 'C:\Repos\maven'
    #     commits = ["778f044e"]
    #     get_commit_2_methods_metric(repo_path, commits, None)

    def test_repo_checkout_commit(self):
        repo_url = "https://github.com/apache/maven.git"
        repo_path = "C:\\temp\\tmp_repo"
        # get_commit_2_methods_metric_2(repo_url, ["778f044e"])
        extractor = MetricExtractor(repo_url, repo_path)
        repo = Repo(repo_path)
        self.assertTrue(not repo.bare)
        extractor.checkout("778f044e")
        commit = repo.head.commit
        t = 1


if __name__ == '__main__':
    unittest.main()
