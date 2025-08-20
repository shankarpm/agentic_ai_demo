from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseMLSAdapter(ABC):
    @abstractmethod
    def list_properties(self) -> List[Dict[str, Any]]:
        ...

    @abstractmethod
    def get_property(self, pid: str) -> Dict[str, Any]:
        ...
