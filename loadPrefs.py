# -*- coding: utf-8 -*-

import ast

def load_preferences(): #will retrieve some custom setting from a conf file, that the users may want to change (e.g. presence of some features, colors, ...)
    config = {}
    with open("resources/data/preferences.conf", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if len(line)>0 and not line.startswith("#"): #not a comment or empty line
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                config[key] = ast.literal_eval(value)
    return config
