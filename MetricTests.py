import os
import re
import shutil
import unittest
from os import listdir, path

from git import Repo

from RepoExtractorPlugin import JavaCallGraphMetricFileExtractorPlugin
from RepoMetricExtractor import get_commit_2_methods_metric_2, MetricExtractor


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

    def test_maven_repo_generate_raw_metric(self):
        # repo_url = "https://github.com/apache/maven.git"
        # extractor = MetricExtractor(repo_url, self.repo_path)
        # repo = Repo(self.repo_path)
        # self.assertTrue(not repo.bare)
        commit_id = "56cd921f"
        # extractor.checkout(commit_id)
        # commit = repo.head.commit
        # self.assertTrue(commit_id in str(commit))
        tool = "C:\\Java_analysis\\java-callgraph-master\\target\\javacg-0.1-SNAPSHOT-static.jar"
        raw_tool_file_extractor = JavaCallGraphMetricFileExtractorPlugin(tool)
        out_file = "{}.txt".format(commit_id)
        out_path = self.raw_metric_files_folder + os.path.sep + out_file
        java_exe = 'C:\\Program Files\\Java\\jdk1.8.0_291\\bin\\java.exe'
        raw_tool_file_extractor.tool_generate_metric(java_exe, commit_id, self.repo_path, out_path)

    def test_maven_repo_generate_all_raw_metric(self):
        folder_with_commits_files = "C:\\My_Stuff\\BGU\\לימודים\\2021\\איתור תקלות\\פרויקט\\maven_data\\matrices"
        # folder_with_commits_files = "C:\\My_Stuff\\BGU\\לימודים\\2021\\איתור תקלות\\פרויקט\\wicket_data\\matrices"
        files = listdir(folder_with_commits_files)
        commits = []
        for file in files:
            commits.append(file.split('_')[1])

        repo_url = "https://github.com/apache/maven.git"
        # repo_url = "https://github.com/apache/wicket.git"
        tool = "C:\\Java_analysis\\java-callgraph-master\\target\\javacg-0.1-SNAPSHOT-static.jar"
        java_exe = 'C:\\Program Files\\Java\\jdk1.8.0_291\\bin\\java.exe'
        for commit_id in commits:
            extractor = MetricExtractor(repo_url, self.repo_path)
            repo = Repo(self.repo_path)
            self.assertTrue(not repo.bare)
            extractor.checkout(commit_id)
            commit = repo.head.commit
            self.assertTrue(commit_id in str(commit))

            raw_tool_file_extractor = JavaCallGraphMetricFileExtractorPlugin(tool)
            out_file = "{}.txt".format(commit_id)
            out_path = self.raw_metric_files_folder + os.path.sep + out_file
            raw_tool_file_extractor.tool_generate_metric(java_exe, commit_id, self.repo_path, out_path)

    def test_wicket_repo_checkout_commit(self):
        repo_url = "https://github.com/apache/wicket.git"
        extractor = MetricExtractor(repo_url, self.repo_path)
        repo = Repo(self.repo_path)
        self.assertTrue(not repo.bare)
        commit_id = "f45ce896"
        extractor.checkout(commit_id)
        commit = repo.head.commit
        self.assertTrue(commit_id in str(commit))
        # extractor.remove_repo()

    def test_wicked_repo_generate_all_jars(self):
        folder_with_commits_files = "C:\\My_Stuff\\BGU\\לימודים\\2021\\איתור תקלות\\פרויקט\\wicket_data\\matrices"
        files = listdir(folder_with_commits_files)
        commits = []
        for file in files:
            commits.append(file.split('_')[1])
        repo_url = "https://github.com/apache/wicket.git"
        commits_unsuccessful = []
        for commit_id in commits:
            commit_output_folder = self.wicket_jars_folder + path.sep + str(commit_id)
            if not os.path.exists(commit_output_folder):
                os.makedirs(commit_output_folder)
            else:
                continue

            extractor = MetricExtractor(repo_url, self.repo_path)
            repo = Repo(self.repo_path)
            self.assertTrue(not repo.bare)
            extractor.checkout(commit_id)
            commit = repo.head.commit
            self.assertTrue(commit_id in str(commit))



            try:
                import subprocess
                # cmd: mvn -Dmaven.javadoc.skip=true -Dmaven.test.skip=true package
                # subprocess.check_output(['mvn', 'clean'], shell=True, cwd=self.repo_path)
                subprocess.check_output(['mvn', '-Dmaven.javadoc.skip=true', '-Dmaven.test.skip=true',
                                         'package'], shell=True, cwd=self.repo_path)

                regex = re.compile('(.*jar$)')
                jar_folder = self.repo_path + os.path.sep + 'wicket-core' + os.path.sep + 'target'
                jars = []
                only_files = [f for f in listdir(jar_folder) if path.isfile(path.join(jar_folder, f))]
                for file in only_files:
                    if regex.match(file):
                        jars.append(path.join(jar_folder, file))

                for jar in jars:
                    shutil.copy2(jar, commit_output_folder)

                # jar_file = self.repo_path + os.path.sep + 'wicket-core' + os.path.sep + 'target' + os.path.sep + 'wicket-core-7.0.0-SNAPSHOT.jar'
            except Exception as e:
                print(commit_id, e)
                commits_unsuccessful.append(commit_id)

        print("commits_unsuccessful", commits_unsuccessful)

    def test_wicket_repo_generate_all_raw_metric(self):
        # folder_with_commits_files = "C:\\My_Stuff\\BGU\\לימודים\\2021\\איתור תקלות\\פרויקט\\maven_data\\matrices"
        folder_with_commits_files = "C:\\My_Stuff\\BGU\\לימודים\\2021\\איתור תקלות\\פרויקט\\wicket_data\\matrices"
        files = listdir(folder_with_commits_files)
        commits = []
        for file in files:
            commits.append(file.split('_')[1])

        tool = "C:\\Java_analysis\\java-callgraph-master\\target\\javacg-0.1-SNAPSHOT-static.jar"
        java_exe = 'C:\\Program Files\\Java\\jdk1.8.0_291\\bin\\java.exe'
        wicket_jars_folder = 'C:\\temp\\wicket_jars'
        for commit_id in commits:
            commit_jar_folder = wicket_jars_folder + path.sep + commit_id
            raw_tool_file_extractor = JavaCallGraphMetricFileExtractorPlugin(tool, jar_regex='(.*SNAPSHOT.jar$)')
            out_file = "{}.txt".format(commit_id)
            out_path = self.raw_metric_files_folder + os.path.sep + out_file
            raw_tool_file_extractor.tool_generate_metric(java_exe, commit_id, commit_jar_folder, out_path)


    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == '__main__':
    unittest.main()
