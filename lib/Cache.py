import json
from functools import lru_cache

from lib.sql import session_scope, DataTable


class SomeFreeSpace:
    def __init__(self, server_id):
        self.server_id = server_id

    def get_description(self):
        infos = servers()[int(self.server_id)]
        description = infos["description"]
        if description:
            return description

    def get_invite(self):
        infos = servers()[int(self.server_id)]
        invite = infos["server_invite"]
        if invite:
            return invite


@lru_cache()
def servers():
    server_cache = {}
    with session_scope() as db_session:
        room_data = db_session.query(DataTable)
        room_table = [p.dump() for p in room_data]
        print("[DATENBANK] >> Server Cache wird geladen")
        for i in room_table:
            server_cache[int(i["server_id"])] = {
                "description": i["text"],
                "author": i["author"],
                "img_url": i["img_url"],
                "server_invite": i["server_invite"],
                "channel_id": i["channel_id"]
            }
    return server_cache


@lru_cache()
def channels():
    server_cache = []
    with session_scope() as db_session:
        room_data = db_session.query(DataTable)
        room_table = [p.dump() for p in room_data]
        print("[DATENBANK] >> Channel Cache wird geladen")
        for i in room_table:
            server_cache.append(i["channel_id"])
    return server_cache


@lru_cache()
def config():
    with open("config.json", encoding="utf-8") as fp:
        data = json.load(fp)
    return data
