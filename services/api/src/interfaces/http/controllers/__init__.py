from interfaces.http.controllers import sessions as _sessions
from interfaces.http import config

_config = config.load()
sessions = _sessions.Controller(_config)
