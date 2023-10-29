import json


class VersionManager:
    def __init__(self, version_config):
        with open(version_config) as f:
            self.version_dict = json.load(f)

    def get_versions(self, model: str) -> dict:
        # model could be RTX 4090, could be PSU
        # returns a dict of versions with reference prices
        return self.version_dict.get(model, {})

    def get_version_price(self, model, version):
        return self.get_versions(model).get(version, 0)
