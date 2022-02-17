from interfaces.http.middleware import authentication as _authentication
from interfaces.http import config
from interfaces.http import validation as v

_config = config.load()
_validator = v.load_validator(_config)
authentication = _authentication.create_middleware(_config, _validator)
