import os
import shutil

import git
from typing import List

from git import Repo

from RepoExtractorPlugin import MetricExtractorPlugin


def print_commit(commit):
    print('----')
    print(str(commit.hexsha))
    print("\"{}\" by {} ({})".format(commit.summary,
                                     commit.author.name,
                                     commit.author.email))
    print(str(commit.authored_datetime))
    print(str("count: {} and size: {}".format(commit.count(), commit.size)))


def print_repository(repo):
    print('Repo description: {}'.format(repo.description))
    print('Repo active branch is {}'.format(repo.active_branch))
    for remote in repo.remotes:
        print('Remote named "{}" with URL "{}"'.format(remote, remote.url))
    print('Last commit for repo is {}.'.format(str(repo.head.commit.hexsha)))




def get_commit_2_methods_metric(repo_path: str, commits: List[str], metric_tool: MetricExtractorPlugin):
    #g = git.cmd.Git("git_dir")
    repo = Repo(repo_path)
    # check that the repository loaded correctly
    if not repo.bare:
        print('Repo at {} successfully loaded.'.format(repo_path))
        print_repository(repo)
        # create list of commits then print some of them to stdout
        commits = list(repo.iter_commits('master'))[:2]
        for commit in commits:
            print_commit(commit)
            pass
    else:
        print('Could not load repository at {} :('.format(repo_path))


def get_commit_2_methods_metric_2(repo_url: str, commits: List[str], metric_tool: MetricExtractorPlugin = None):
    # "https://github.com/apache/maven.git"
    repo = git.Repo.clone_from(repo_url, "C:\\temp\\tmp_repo", no_checkout=True)
    repo.git.checkout(commits[0])


class MetricExtractor(object):
    def __init__(self, repo_url: str, repo_path: str = None):
        self.repo_url = repo_url
        self.__repo_path = "C:\\temp\\tmp_repo"
        if repo_path:
            self.__repo_path = repo_path
        if os.path.exists(self.__repo_path):
            shutil.rmtree(self.__repo_path)
        self.repo = git.Repo.clone_from(repo_url, self.__repo_path, no_checkout=True)

    def checkout(self, commit: str):
        self.repo.git.checkout(commit)

    def analyze(self, metric_plugin: MetricExtractorPlugin):
        metric_plugin.tool_analyse(self.__repo_path)

    def __del__(self):
        if not os.path.exists(self.__repo_path):
            return
        shutil.rmtree(self.__repo_path)
