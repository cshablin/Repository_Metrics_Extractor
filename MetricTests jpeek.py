import os
import re
import shutil
import unittest
from os import listdir, path

from git import Repo

from RepoExtractorPlugin import JavaCallGraphMetricFileExtractorPlugin, JPeekMetricFileExtractorPlugin
from RepoMetricExtractor import get_commit_2_methods_metric_2, MetricExtractor
import subprocess

class MyTestCase(unittest.TestCase):

    repo_path = "C:\\temp\\tmp_repo"
    raw_metric_files_folder = "C:\\temp\\raw_metric_files"
    wicket_jars_folder = "C:\\temp\\wicket_jars"

    def test_maven_repo_checkout_commit(self):
        repo_url = "https://github.com/apache/maven.git"
        extractor = MetricExtractor(repo_url, self.repo_path)
        repo = Repo(self.repo_path)
        self.assertTrue(not repo.bare)
        commit_id = "56cd921f"
        extractor.checkout(commit_id)
        commit = repo.head.commit
        self.assertTrue(commit_id in str(commit))
        # extractor.remove_repo()

    def test_maven_repo_generate_raw_metric_jpeek(self):
        print('test jpeek')
        repo_url = "https://github.com/apache/maven.git"
        # repo_path = "C:\\temp\\tmp_repo_2eb419ed"
        extractor = MetricExtractor(repo_url, self.repo_path)
        repo = Repo(self.repo_path)
        self.assertTrue(not repo.bare)
        commit_id = "2eb419ed" #"56cd921f"
        extractor.checkout(commit_id)
        print('')
        commit = repo.head.commit
        self.assertTrue(commit_id in str(commit))
        tool = "C:\Dev\diagnose_project\\jpeek-jar-with-dependencies.jar"
        raw_tool_file_extractor = JPeekMetricFileExtractorPlugin(tool)
        out_path = self.raw_metric_files_folder + os.path.sep + str(commit_id)
        java_exe = 'C:\\Program Files\\Java\\jdk1.8.0_291\\bin\\java.exe'
        raw_tool_file_extractor.tool_generate_metric(java_exe, commit_id, self.repo_path, out_path)

    def test_maven_repo_generate_all_raw_metric_jpeek(self):
        print(' start maben analysis')
        folder_with_commits_files = "C:\\Users\\User\diagnosis\\\maven_data\matrices"
        files = listdir(folder_with_commits_files)
        commits = []
        for file in files:
            commits.append(file.split('_')[1])

        repo_url = "https://github.com/apache/maven.git"
        # repo_url = "https://github.com/apache/wicket.git"
        extractor = MetricExtractor(repo_url, self.repo_path)
        tool = "C:\Dev\diagnose_project\\jpeek-jar-with-dependencies.jar"
        raw_tool_file_extractor = JPeekMetricFileExtractorPlugin(tool)
        java_exe = 'C:\\Program Files\\Java\\jdk1.8.0_291\\bin\\java.exe'
        for commit_id in commits:
            print(commit_id)

            repo = Repo(self.repo_path)
            self.assertTrue(not repo.bare)
            extractor.checkout(commit_id)
            commit = repo.head.commit
            self.assertTrue(commit_id in str(commit))

            out_path = self.raw_metric_files_folder + os.path.sep + str(commit_id)
            p = subprocess.Popen('mvn clean compile', cwd= self.repo_path, shell=True)
            p.wait()
            raw_tool_file_extractor.tool_generate_metric(java_exe, commit_id, self.repo_path, out_path)

    def test_wicket_repo_generate_all_raw_metric_jpeek(self):
        print(' start wicket analysis')
        folder_with_commits_files = "C:\\Users\\User\diagnosis\\\wicket_data\matrices"
        files = listdir(folder_with_commits_files)
        commits = []
        for file in files:
            commits.append(file.split('_')[1])

        repo_url = "https://github.com/apache/wicket.git"
        extractor = MetricExtractor(repo_url, self.repo_path)
        tool = "C:\Dev\diagnose_project\\jpeek-jar-with-dependencies.jar"
        raw_tool_file_extractor = JPeekMetricFileExtractorPlugin(tool)
        java_exe = 'C:\\Program Files\\Java\\jdk1.8.0_291\\bin\\java.exe'
        for commit_id in commits:
            print(commit_id)

            repo = Repo(self.repo_path)
            self.assertTrue(not repo.bare)
            extractor.checkout(commit_id)
            commit = repo.head.commit
            self.assertTrue(commit_id in str(commit))

            out_path = self.raw_metric_files_folder_wicket + os.path.sep + str(commit_id)
            p = subprocess.Popen('mvn clean compile', cwd= self.repo_path, shell=True)
            p.wait()
            raw_tool_file_extractor.tool_generate_metric(java_exe, commit_id, self.repo_path, out_path)

if __name__ == '__main__':
    unittest.main()
