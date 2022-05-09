from time import time as tm

from lib.Cache import servers
from lib.JsonThings import JsonHandling
from lib.sql import session_scope, DataTable



class ServerThings:
    def __init__(self, server_id: int):
        self.server_id = server_id

    def create_server(self, img_url: str = None):
        with session_scope() as db_session:
            if not self.get_server():
                new_server = DataTable(
                    server_id=self.server_id,
                    count=0,
                    text="",
                    author="",
                    img_url=img_url,
                    channel_id=0,
                    server_invite=""
                )
                db_session.add(new_server)

    def get_server(self):
        return self.server_id in servers()

    def delete_server(self):
        with session_scope() as db_session:
            if self.get_server():
                db_session.query(DataTable).filter_by(server_id=self.server_id).delete()


class ChannelThings(ServerThings):
    def __init__(self, server_id: int):
        super().__init__(server_id)
        self.server_id = server_id

    def set_channel(self, channel_id: int):
        with session_scope() as db_session:
            db_session.query(DataTable).filter_by(server_id=self.server_id) \
                .update({'channel_id': channel_id})

    def reset_channel(self):
        with session_scope() as db_session:
            db_session.query(DataTable).filter_by(server_id=self.server_id) \
                .update({'channel_id': 0})

    def delete_specific_channel(self, channel_id):
        with session_scope() as db_session:
            db_session.query(DataTable).filter_by(channel_id=channel_id)


class DescriptionStuff(ServerThings):
    def __init__(self, server_id: int, description: str):
        super().__init__(server_id)
        self.description = description

    def set_description(self):
        self.create_server()
        with session_scope() as db_session:
            db_session.query(DataTable).filter_by(server_id=self.server_id) \
                .update({'text': self.description})

    def delete_description(self):
        with session_scope() as db_session:
            db_session.query(DataTable).filter_by(server_id=self.server_id) \
                .update({'text': ""})


class InviteStuff:
    def __init__(self, server_id, invite: str):
        self.server_id = server_id
        self.invite = invite

    def set_invite(self):
        with session_scope() as db_session:
            db_session.query(DataTable).filter_by(server_id=self.server_id) \
                .update({'server_invite': self.invite})

    def get_invite(self):
        with session_scope() as db_session:
            data = db_session.query(DataTable).filter_by(server_id=self.server_id).first()
            if data.invite != "":
                return True


class BumpStuff(ServerThings):
    def __init__(self, server_id: int):
        super().__init__(server_id)

    def bump(self):
        if self.get_server():
            time = JsonHandling(str(self.server_id)).get_time()
            print(round(tm() - time), "time")
            if servers()[self.server_id]["description"]:
                if round(tm() - time) > 31600:  # maybe wrong TODO("austesten")
                    with session_scope() as db_session:
                        db_session.query(DataTable).filter_by(server_id=self.server_id) \
                            .update({'count': DataTable.count + 1})
                    return "a"
                else:
                    return "b"
            else:
                return "c"
