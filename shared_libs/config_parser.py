import json
import os


class configParser:
    def __init__(self, configFile=None):
        if not os.path.exists(configFile):
            raise Exception('config file not exists')
        if not os.path.isfile(configFile):
            raise Exception('the {} is not file type'.format(configFile))

        self.configfilePath = configFile
        self.configfileRaw = json.loads(open(self.configfilePath, 'r').read())

    def get_globals(self):
        return self.configfileRaw['globals']

    def get_global_keys(self):
        return list(self.configfileRaw['globals'].keys())

    def get_envs(self):
        return list(self.configfileRaw.keys())

    def get_key_from_glob(self, key):
        if self.configfileRaw['globals'].get(key) is not None:
            return self.configfileRaw['globals'][key]
        raise KeyError('{}: no such key'.format(key))

    def get_key(self, env=None, key=None):
        if env is None:
            return self.get_key_from_glob(key)

        if self.configfileRaw['envs'].get(env) is None:
            return self.get_key_from_glob(key)

        if key is None:
            raise TypeError('{} key required in env: {}'.format(key, env))

        if self.configfileRaw['envs'][env].get(key) is None:
            try:
                return self.get_key_from_glob(key)
            except TypeError:
                raise TypeError(
                    '{} not exists not in global and not in specified env')

        return self.configfileRaw['envs'][env][key]
