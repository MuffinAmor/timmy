import json
import os
from time import time


class JsonHandling:
    def __init__(self, server_id: str):
        self.server_id = server_id

    def get_time(self):
        with open("time.json", encoding="utf-8") as fp:
            data = json.load(fp)
        if self.server_id in data:
            return data[self.server_id]
        else:
            data[self.server_id] = 21601
            with open("time.json", "w+") as fp:
                json.dump(data, fp, indent=4)
            return data[self.server_id]

    def edit_time(self):
        with open("time.json", encoding="utf-8") as fp:
            data = json.load(fp)
        print(data, "yeet")
        if self.server_id in data:
            data[self.server_id] = time()
            with open("time.json", "w+") as fp:
                json.dump(data, fp, indent=4)
            return data[self.server_id]
        else:
            raise KeyError("Server not found")
