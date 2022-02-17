import os
import functools
from typing import Dict, Optional
from dataclasses import dataclass

env_vars = [
    "SECRET_KEY",
    "DATABASE_USERNAME",
    "DATABASE_PASSWORD",
    "DATABASE_NAME",
    "DATABASE_TEST_USERNAME",
    "DATABASE_TEST_PASSWORD",
    "DATABASE_TEST_NAME",
    "DATABASE_HOST",
    "TOKEN_STORE_USERNAME",
    "TOKEN_STORE_PASSWORD",
    "TOKEN_STORE_NAME",
    "TOKEN_STORE_TEST_USERNAME",
    "TOKEN_STORE_TEST_PASSWORD",
    "TOKEN_STORE_TEST_NAME",
    "TOKEN_STORE_HOST",
    "MAXIMUM_USERNAME_LENGTH",
    "MAXIMUM_PASSWORD_LENGTH",
    "MINIMUM_USERNAME_LENGTH",
    "MINIMUM_PASSWORD_LENGTH",
]


@dataclass
class Config:
    SECRET_KEY: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_HOST: str
    TOKEN_STORE_USERNAME: str
    TOKEN_STORE_PASSWORD: str
    TOKEN_STORE_NAME: str
    TOKEN_STORE_HOST: str
    MAXIMUM_USERNAME_LENGTH: int = 30
    MINIMUM_USERNAME_LENGTH: int = 3
    MAXIMUM_PASSWORD_LENGTH: int = 100
    MINIMUM_PASSWORD_LENGTH: int = 16


@dataclass
class ConfigFactory:
    SECRET_KEY: Optional[str]
    DATABASE_USERNAME: Optional[str]
    DATABASE_PASSWORD: Optional[str]
    DATABASE_NAME: Optional[str]
    DATABASE_TEST_USERNAME: Optional[str]
    DATABASE_TEST_PASSWORD: Optional[str]
    DATABASE_TEST_NAME: Optional[str]
    DATABASE_HOST: Optional[str]
    TOKEN_STORE_USERNAME: Optional[str]
    TOKEN_STORE_PASSWORD: Optional[str]
    TOKEN_STORE_NAME: Optional[str]
    TOKEN_STORE_TEST_USERNAME: Optional[str]
    TOKEN_STORE_TEST_PASSWORD: Optional[str]
    TOKEN_STORE_TEST_NAME: Optional[str]
    TOKEN_STORE_HOST: Optional[str]
    MAXIMUM_USERNAME_LENGTH: Optional[str]
    MINIMUM_USERNAME_LENGTH: Optional[str]
    MAXIMUM_PASSWORD_LENGTH: Optional[str]
    MINIMUM_PASSWORD_LENGTH: Optional[str]

    def load(self, test: bool = False, privileged: bool = False) -> Config:
        env_vars = {
            "SECRET_KEY": self.SECRET_KEY,
            "MAXIMUM_USERNAME_LENGTH": self.MAXIMUM_USERNAME_LENGTH,
            "MINIMUM_USERNAME_LENGTH": self.MINIMUM_USERNAME_LENGTH,
            "MAXIMUM_PASSWORD_LENGTH": self.MAXIMUM_PASSWORD_LENGTH,
            "MINIMUM_PASSWORD_LENGTH": self.MAXIMUM_USERNAME_LENGTH,
        }
        if privileged:
            env_vars |= {
                "DATABASE_USERNAME": self.DATABASE_TEST_USERNAME,
                "DATABASE_PASSWORD": self.DATABASE_TEST_PASSWORD,
                "DATABASE_NAME": self.DATABASE_TEST_NAME,
                "DATABASE_HOST": self.DATABASE_HOST,
                "TOKEN_STORE_USERNAME": self.TOKEN_STORE_TEST_USERNAME,
                "TOKEN_STORE_PASSWORD": self.TOKEN_STORE_TEST_PASSWORD,
                "TOKEN_STORE_NAME": self.TOKEN_STORE_TEST_NAME,
                "TOKEN_STORE_HOST": self.TOKEN_STORE_HOST,
            }
        elif test:
            env_vars |= {
                "DATABASE_USERNAME": self.DATABASE_USERNAME,
                "DATABASE_PASSWORD": self.DATABASE_PASSWORD,
                "DATABASE_NAME": self.DATABASE_TEST_NAME,
                "DATABASE_HOST": self.DATABASE_HOST,
                "TOKEN_STORE_USERNAME": self.TOKEN_STORE_USERNAME,
                "TOKEN_STORE_PASSWORD": self.TOKEN_STORE_PASSWORD,
                "TOKEN_STORE_NAME": self.TOKEN_STORE_TEST_NAME,
                "TOKEN_STORE_HOST": self.TOKEN_STORE_HOST,
            }
        else:
            env_vars |= {
                "DATABASE_USERNAME": self.DATABASE_USERNAME,
                "DATABASE_PASSWORD": self.DATABASE_PASSWORD,
                "DATABASE_NAME": self.DATABASE_NAME,
                "DATABASE_HOST": self.DATABASE_HOST,
                "TOKEN_STORE_USERNAME": self.TOKEN_STORE_USERNAME,
                "TOKEN_STORE_PASSWORD": self.TOKEN_STORE_PASSWORD,
                "TOKEN_STORE_NAME": self.TOKEN_STORE_NAME,
                "TOKEN_STORE_HOST": self.TOKEN_STORE_HOST,
            }
        env_vars = {
            e: env_vars[e] for e in env_vars if env_vars[e] is not None
        }
        return Config(**env_vars)


@functools.lru_cache
def read_raw_environment_variables() -> Dict:
    return {env_var: os.getenv(env_var) for env_var in env_vars}


def initialize_config_factory():
    raw_env_vars = read_raw_environment_variables()
    config_factory = ConfigFactory(**raw_env_vars)
    return config_factory
