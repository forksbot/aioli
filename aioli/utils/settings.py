# -*- coding: utf-8 -*-

import os
import yaml


def yaml_parse(file, keys_to_upper=False):
    settings_dir = os.environ.get("JET_SETTINGS_DIR", "settings")
    path = f"{settings_dir}/{file}"

    with open(path, "r") as stream:
        for key, value in yaml.load(stream).items():
            if keys_to_upper:
                yield key.upper(), value
            else:
                yield key, value
