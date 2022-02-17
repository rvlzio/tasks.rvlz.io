from config import Config, initialize_config_factory


def load() -> Config:
    config_factory = initialize_config_factory()
    return config_factory.load()
