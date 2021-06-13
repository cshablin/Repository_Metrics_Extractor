import re
from abc import ABC, abstractmethod
from os import listdir
from os.path import isfile, join
from typing import List, Dict, Tuple


class MetricExtractorPlugin(ABC):

    @abstractmethod
    def __init__(self, tool_exe: str, interest_methods: List[str]):
        self._tool_exe = tool_exe
        self._interest_methods = interest_methods

    @abstractmethod
    def tool_analyse(self, repo_root_folder: str, *args) -> None:
        pass

    @property
    @abstractmethod
    def method_metrics(self) -> Dict[Tuple[str, str], float]:
        pass


class MetricRawFileExtractorPlugin(ABC):

    @abstractmethod
    def __init__(self, tool_exe: str):
        self._tool_exe = tool_exe

    @abstractmethod
    def tool_generate_metric(self, java_exe: str, commit_id: str, repo_root_folder: str, out_file_path: str, *args) -> None:
        pass


class JavaCallGraphMetricFileExtractorPlugin(MetricRawFileExtractorPlugin):

    def __init__(self, tool_exe: str, jar_regex: str = '(.*jar$)'):
        super(JavaCallGraphMetricFileExtractorPlugin, self).__init__(tool_exe)
        self.jar_regex = jar_regex
        # cmd "java -jar javacg-0.1-SNAPSHOT-static.jar C:\temp\tmp_repo\maven-ant-tasks-2.1.1.jar > myoutput.txt"

    def tool_generate_metric(self, java_exe: str, commit_id: str, jar_folder: str, out_file_path: str, *args) -> None:
        regex = re.compile(self.jar_regex)
        jars = []
        only_files = [f for f in listdir(jar_folder) if isfile(join(jar_folder, f))]
        for file in only_files:
            if regex.match(file):
                jars.append(join(jar_folder, file))

        try:
            assert len(jars) == 1
            import subprocess
            subprocess.check_output([java_exe, '-jar', self._tool_exe, jars[0], '>', out_file_path], shell=True)
        except Exception as e:
            print(e)


class JPeekMetricFileExtractorPlugin(MetricRawFileExtractorPlugin):
    def __init__(self, tool_exe: str):
        super().__init__(tool_exe)
        # cmd " java -jar jpeek-jar-with-dependencies.jar --sources . --target ./jpeek"

    def tool_generate_metric(self, java_exe: str, commit_id: str, repo_root_folder: str, out_path: str) :
        regex = re.compile('(.*jar$)')
        jars = []
        only_files = [f for f in listdir(repo_root_folder) if isfile(join(repo_root_folder, f))]
        for file in only_files:
            if regex.match(file):
                jars.append(join(repo_root_folder, file))
        print(len(jars))
        print(repo_root_folder)
        print(jars)
        assert len(jars) == 1
        try:

            print('run command: '+' '.join([java_exe, '-jar', self._tool_exe, '--sources', repo_root_folder ,'--target', out_path]))
            subprocess.check_output([java_exe, '-jar', self._tool_exe, '--sources', repo_root_folder ,'--target', out_path], shell=True)
        except Exception as e:
            print(e)