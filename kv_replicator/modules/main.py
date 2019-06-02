import consul
from config_parser import configParser
from misc_funcs import myenv
import re
import os
from threader import Threader
from queuer import Queuer
import time
from requests import exceptions as rexptions


class defaults(configParser):
    def __init__(self):
        configParser.__init__(self, configFile="./config/config.json")
        self.runenv = myenv()
        self.consul_instance = self._consul_setup_connect(host=self.get_key(env=self.runenv, key="consulHost"),
                                                          scheme=self.get_key_from_glob("consul")['scheme'],
                                                          port=self.get_key_from_glob("consul")['port'])
        self.proxy_instance = self._consul_setup_connect(host=self.get_key(env=self.runenv, key="proxy")['host'],
                                                         scheme=self.get_key(env=self.runenv, key="proxy")["scheme"],
                                                         port=self.get_key(env=self.runenv, key="proxy")['port'])

        self.read_token = self.get_key_from_glob("general_read_token")
        self.write_token = self.get_key(env=self.runenv, key="write_token")

        self.prefixes = self._get_prefixes()


    def _get_prefixes(self):
        if not os.path.exists(self.get_key_from_glob("prefix_file")) and not os.path.isfile(
                self.get_key_from_glob("prefix_file")):
            raise Exception("No prefix file provided")

        with open(self.get_key_from_glob("prefix_file"), "r") as srcf:
            prefixes = srcf.readlines()
            prefixes = [x.strip('\n') for x in prefixes]
            return prefixes


    def _check_consul_connect(self, obj):
        if obj.status.peers():
            return True
        return None


    def _consul_setup_connect(self, host, scheme, port):
        try:
            if type(host) is list:
                for h in host:
                    try:
                        c = consul.Consul(host=h, scheme=scheme, port=port)
                        c.connect(host=h, port=port, scheme=scheme)
                        if self._check_consul_connect(c) is True:
                            return c
                    except rexptions.ConnectionError:
                        pass

            elif type(host) is str:
                c = consul.Consul(host=host, scheme=scheme, port=port)
                c.connect(host=host, port=port, scheme=scheme)
                if self._check_consul_connect(c) is True:
                    return c
            raise Exception('Failed to connect to {}://{}:{}'.format(scheme,host,port))
        except rexptions.SSLError:
            if type(host) is list:
                for h in host:
                    c = consul.Consul(host=h, scheme=scheme, port=port, verify=False)
                    c.connect(host=h, port=port, scheme=scheme, verify=False)
                    if self._check_consul_connect(c) is True:
                        return c
            elif type(host) is str:
                c = consul.Consul(host=host, scheme=scheme, port=port, verify=False)
                c.connect(host=host, port=port, scheme=scheme, verify=False)
                if self._check_consul_connect(c) is True:
                    return c
            raise Exception('Failed to connect to {}://{}:{}'.format(scheme, host, port))

class getAndPut(defaults, Threader, Queuer):
    def __init__(self):
        defaults.__init__(self)
        Queuer.__init__(self)
        Threader.__init__(self, threadmax=self.get_key_from_glob("MAX_THREADS"))
        self.patt = self.get_key_from_glob("kv_prefix")
        self.bringup_daemon(self._update_consule, self.main_q)

    def get_matching_keys(self):
        for prefix in self.prefixes:
            res = self.proxy_instance.kv.get(prefix, recurse=True, keys=True, token=self.read_token)
            if res:
                for entry in res[-1]:
                    if re.match(self.patt, entry):
                        print(entry)
                        self.add_to_q(entry)
        return True

    def _update_consule(self, item):
        try:
            val = self.proxy_instance.kv.get(item, token=self.read_token)
            self.consul_instance.kv.put(key=item, value=val[-1]['Value'], token=self.write_token)

            return True

        except Exception as e:
            raise e


def main():

    while True:
        workload = getAndPut()
        workload.get_matching_keys()
        time.sleep(workload.get_key_from_glob("timeout"))


"""TODO: Make sure it exits fast ! no wait to much, test in prod"""