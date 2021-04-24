from abc import ABC, abstractmethod
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
