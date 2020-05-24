import json
import os
from time import time

import requests

os.chdir(r'/home/niko/data/')

def self_token():
    with open("Timmy/token.json", 'r') as fp:
        data = json.load(fp)
    return data['dbl']

def create_time(server_id: str):
    if not os.path.isfile("Timmy"):
        try:
            os.mkdir("Timmy")
        except:
            pass
    if not os.path.isfile("Timmy/time.json"):
        data = {server_id: time()}
        with open("Timmy/time.json", "w+") as fp:
            json.dump(data, fp, indent=4)


def get_time(server_id: str):
    create_time(server_id)
    if os.path.isfile("Timmy/time.json"):
        with open("Timmy/time.json", encoding="utf-8") as fp:
            data = json.load(fp)
        if str(server_id) in data:
            return data[server_id]
        else:
            data[server_id] = 21601
            with open("Timmy/time.json", "w+") as fp:
                json.dump(data, fp, indent=4)
            return data[server_id]
    else:
        return None


def edit_time(server_id: str):
    create_time(server_id)
    if os.path.isfile("Timmy/time.json"):
        with open("Timmy/time.json", encoding="utf-8") as fp:
            data = json.load(fp)
        if str(server_id) in data:
            data[server_id] = time()
            with open("Timmy/time.json", "w+") as fp:
                json.dump(data, fp, indent=4)
            return data[server_id]
        else:
            data[server_id] = 21601
            with open("Timmy/time.json", "w+") as fp:
                json.dump(data, fp, indent=4)
            return data[server_id]
    else:
        return None


def check_dbl_vote(user_id: str):
    header = {
        'Authorization': self_token()}
    r = requests.get(
        "https://top.gg/api/bots/631149480464613406/check?userId=%s" % (user_id), headers=header)
    data = r.json()
    try:
        voted = data['voted']
    except KeyError:
        print("KeyError")
        voted = 0
    if str(voted) == "1":
        return True
    elif str(voted) == "0":
        return False
