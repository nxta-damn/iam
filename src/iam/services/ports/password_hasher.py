from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    @abstractmethod
    def hash_password(self, raw_password: str) -> bytes: ...
    @abstractmethod
    def check_password(self, raw_password: str, hashed_password: bytes) -> bool: ...
