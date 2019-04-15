import json
from jwkest.jws import JWS
from jwkest.jwk import SYMKey


class JwtCreator:
    def __init__(self, map, alg, config):
        self.map = map
        self.jws = JWS(json.dumps(self.map), alg=alg)
        keys = [SYMKey(key=config['api_secret'], alg=alg)]
        self.keys = keys

    def sign_compact(self):
        self.signed = self.jws.sign_compact(keys=self.keys)
        return self.signed
