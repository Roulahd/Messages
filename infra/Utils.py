import os
import yaml


class Utils(object):

    @staticmethod
    def get_params():
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        config_file = dir_path + '/../config.yaml'
        with open(config_file, 'r') as yaml_config:
            cfg = yaml.load(yaml_config)
        return cfg
