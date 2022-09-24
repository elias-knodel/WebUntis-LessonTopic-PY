import json
from pathlib import Path
from datetime import date

today_string = str(date.today())
base = {
    "latestUpdate": today_string
}


# Class Webuntis
#
# This class creates and reads json "cache" files.
# Some webunits queries can become very large so this
# is my approach to not get rate limited by them.
class Cache:
    def __init__(self, cache_identifier="webunits"):
        self.cache_id = cache_identifier + ".cache.json"
        self.file = Path(self.cache_id)

    # Writes cache/data to the json file
    def write(self, json_data):
        base['data'] = json_data
        json_object = json.dumps(base, indent=4)
        with open(self.cache_id, "w") as outfile:
            outfile.write(json_object)

    # Checks if the cache is valid or outdated
    # If the cache is not up-to-date it will return false
    def verify(self):
        if not self.file.is_file():
            return False
        with open(self.cache_id, "r") as openfile:
            json_object = json.load(openfile)
        if json_object["latestUpdate"] != today_string:
            return False
        else:
            return True
