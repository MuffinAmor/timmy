import os
import json





def set_channel(sid:str, cid:str):
    if not os.path.isfile("Timmy"):
        try:
            os.mkdir("Timmy")
        except:
            pass
    if not os.path.isfile("Timmy/partner.json"):
        data = {sid:{}}
        data[sid] = cid
        with open("Timmy/partner.json", "w") as fp:
            json.dump(data, fp, indent=4)
        return "Der Channel wurde erfolgreich gesetzt."
    else:
        with open("Timmy/partner.json", "r") as fp:
            data = json.load(fp)
        data[sid] = cid
        with open("Timmy/partner.json", "w") as fp:
            json.dump(data, fp, indent=4)
        return "Der Channel wurde erfolgreich geändert."

def set_desc(author:int, sid:str, desc:str):
    if not os.path.isfile("Timmy"):
        try:
            os.mkdir("Timmy")
        except:
            pass
    if not os.path.isfile("Timmy/Server"):
        try:
            os.mkdir("Timmy/Server")
        except:
            pass
    if not os.path.isfile("Timmy/Server/{}.json".format(sid)):
        data = {"desc":desc,
                "author": author,
                "invite": ""}
        with open("Timmy/Server/{}.json".format(sid), "w") as fp:
            json.dump(data, fp, indent=4)
        return "Die Beschreibung wurde erfolgreich gesetzt!"
    else:
        with open("Timmy/Server/{}.json".format(sid), "r") as fp:
            data = json.load(fp)
        data["desc"] = desc
        data["author"] = author
        with open("Timmy/Server/{}.json".format(sid), "w") as fp:
            json.dump(data, fp, indent=4)
        return "Die Beschreibung wurde erfolgreich geändert!"

def set_invite(sid:str, invite:str):
    if not os.path.isfile("Timmy/Server/{}.json".format(sid)):
        return "Du musst erst ne Serverbeschreibung setzen!"
    elif request_channel(sid) == None:
        return "Du musst erst ne Serverbeschreibung setzen!"
    else:
        with open("Timmy/Server/{}.json".format(sid), "r") as fp:
            data = json.load(fp)
        data["invite"] = invite
        with open("Timmy/Server/{}.json".format(sid), "w") as fp:
            json.dump(data, fp, indent=4)
        return "Einladung erfolgreich eingestellt!"

def request_desc(sid:str):
    if not os.path.isfile("Timmy/Server/{}.json".format(sid)):
        return None
    else:
        with open("Timmy/Server/{}.json".format(sid), "r") as fp:
            data = json.load(fp)
        return data["desc"]


def request_channel(sid:str):
    if not os.path.isfile("Timmy/partner.json"):
        return None
    else:
        with open("Timmy/partner.json", "r") as fp:
            data = json.load(fp)
        if str(sid) in str(data):
            return data[sid]
        else:
            return None

def request_invite(sid:str):
    if not os.path.isfile("Timmy/Server/{}.json".format(sid)):
        return None
    else:
        with open("Timmy/Server/{}.json".format(sid), "r") as fp:
            data = json.load(fp)
        return data["invite"]

def request_author(sid:str):
    if not os.path.isfile("Timmy/Server/{}.json".format(sid)):
        return None
    else:
        with open("Timmy/Server/{}.json".format(sid), "r") as fp:
            data = json.load(fp)
        return data["author"]

def del_channel(sid:str):
    with open("Timmy/partner.json", "r") as fp:
        data = json.load(fp)
    if str(sid) in data:
        del data[sid]
        with open("Timmy/partner.json", "w") as fp:
            json.dump(data, fp, indent=4)
    else:
        return None

def del_desc(sid:str):
    if not os.path.isfile("Timmy/Server/{}.json".format(sid)):
        return None
    else:
        os.remove("Timmy/Server/{}.json".format(sid))
