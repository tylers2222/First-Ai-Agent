from abc import ABC, abstractmethod
from typing import List, Any

class EmailClient(ABC):
    @abstractmethod
    def GetUnreadEmail(self, limit:int) -> List[Any]:
        pass

    @abstractmethod
    def MarkEmailAsRead():
        pass