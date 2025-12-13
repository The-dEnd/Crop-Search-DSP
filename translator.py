#This file is a large dictionnary that manages translation of PyQt messages. It also contains a translation function.
import time
from datetime import datetime
import yaml

try:
    with open("resources/data/language.conf", "r") as f: #retrieve languages
        for line in f:
            line = line.strip()
            if "=" in line:
                var, value = line.split("=", 1)
                var = var.strip()
                value = value.split("#")[0].strip().replace('"','')
                if var == "current_language":
                    current_language = value
                if var == "default_language":
                    default_language = value
except: #it seems that sometims there are access rights issues on the language.conf file (unknozn reason); hence, this failsafe loop defaults languages to English if this happens
    current_language = "en"
    default_language = "en"
    pass


# Dictionary of messages per language
with open("resources/data/translations.yaml", "r", encoding="utf-8") as f:
    translations = yaml.safe_load(f)


def tr(key): #returns the value associated to the key, for current_language
    msg = translations.get(key)
    if not msg: #if the key does not exist, just display the key
        with open("logs.txt", "a") as logFile:
            logFile.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")+"    Translation key "+key+"not found\n")
        return f"[{key}]"
    if current_language in msg: #if current_language has a translation, return current_language
        return msg[current_language]
    else: #if current_language translation is unavailable, return default_language instead
        with open("logs.txt", "a") as logFile:
            logFile.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")+"    Translation key "+key+"not found for language "+current_language+"; defaulting to "+default_language+"\n")
        return msg[default_language]
    return f"[{key}]"