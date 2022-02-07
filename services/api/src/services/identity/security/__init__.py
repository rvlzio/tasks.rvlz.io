from abc import ABC, abstractmethod


class HashingAlgorithm(ABC):
    @abstractmethod
    def run(self, password: str) -> str:
        pass

    @abstractmethod
    def verify(self, password: str, persisted_hash: str) -> bool:
        pass
