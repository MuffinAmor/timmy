import re


class InviteValidation:
    def __init__(self, invite: str):
        self.invite = invite

    def formation(self):
        return not re.match("(?:https?://)?discord(?:app)?\.(?:com/invite|gg)/[a-zA-Z0-9]+/?", self.invite)

    def exist(self, guild_invites):
        return self.invite.split("/")[3] not in [i.code for i in guild_invites]
