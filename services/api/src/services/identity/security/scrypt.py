import os
import typing
import hashlib
import base64

from . import HashingAlgorithm


class Config:
    def __init__(
        self,
        n=2 ** 15,
        r=8,
        p=1,
        salt_size=16,
        maxmem=2 ** 20 * 64,
    ):
        self.n = n
        self.r = r
        self.p = p
        self.salt_size = salt_size
        self.maxmem = maxmem


class Scrypt(HashingAlgorithm):
    def __init__(self, config: Config = Config()):
        self.config = config

    def _generate_hash_bytes(
        self,
        password_bytes: bytes,
        salt_bytes: bytes,
        config: Config,
    ) -> bytes:
        return hashlib.scrypt(
            password=password_bytes,
            salt=salt_bytes,
            n=config.n,
            r=config.r,
            p=config.p,
            maxmem=config.maxmem,
        )

    def _generate_default_hash_bytes(
        self,
        password_bytes: bytes,
        salt_bytes: bytes,
    ) -> bytes:
        return self._generate_hash_bytes(
            password_bytes,
            salt_bytes,
            self.config,
        )

    def _base64_encode(self, *params: typing.Union[bytes, int]) -> str:
        def to_bytes(param):
            if isinstance(param, bytes):
                return param
            return str(param).encode("utf-8")

        components = [
            base64.b64encode(to_bytes(p)).decode("utf-8") for p in params
        ]
        return ".".join(components)

    def _construct_persisted_hash(
        self,
        salt_bytes: bytes,
        hash_bytes: bytes,
    ) -> str:
        return self._base64_encode(
            self.config.n,
            self.config.r,
            self.config.p,
            salt_bytes,
            hash_bytes,
        )

    def run(self, password: str) -> str:
        password_bytes = password.encode("utf-8")
        salt_bytes = os.urandom(self.config.salt_size)
        hash_bytes = self._generate_default_hash_bytes(
            password_bytes,
            salt_bytes,
        )
        return self._construct_persisted_hash(salt_bytes, hash_bytes)

    def _base64_decode(self, *params: str) -> bytes:
        return [base64.b64decode(p) for p in params]

    def _extract_config(self, *params: bytes) -> Config:
        n, r, p = [int(pm.decode("utf-8")) for pm in params]
        return Config(n=n, r=r, p=p)

    def verify(self, password: str, persisted_hash: str) -> bool:
        password_bytes = password.encode("utf-8")
        persisted_hash_components = self._base64_decode(
            *persisted_hash.split("."),
        )
        salt_bytes, hash_bytes = persisted_hash_components[3:]
        config = self._extract_config(*persisted_hash_components[:3])
        password_hash_bytes = self._generate_hash_bytes(
            password_bytes,
            salt_bytes,
            config,
        )
        return hash_bytes == password_hash_bytes
