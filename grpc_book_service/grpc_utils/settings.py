class _ServiceSettings:
    def __init__(self, servicer, service, rpc_paths):
        self.service = service
        self.servicer = servicer
        self.rpc_paths = rpc_paths


class GrpcSettings:
    _default_server_port = 55000
    _default_workers = 5
    _default_meta_keys = {
        "AUTH_USER": "user",
        "JWT": "Authorization"
    }

    def __init__(self, **kwargs):
        self.services = []
        self.server_port = self._default_server_port
        self.workers = self._default_workers
        self.auth_user_metakey = self._default_meta_keys["AUTH_USER"]
        self.rpc_paths = []

    def add_service(self, servicer, service, rpc_paths):
        self.services.append(_ServiceSettings(servicer, service, rpc_paths))


settings = GrpcSettings()
