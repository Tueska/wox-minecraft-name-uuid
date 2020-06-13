# -*- coding: utf-8 -*-

import requests
import json
import time
import urllib
import shutil
import pyperclip
from os import path
from wox import Wox


class HelloWorld(Wox):

    def copyToClipboard(self, value):
        pyperclip.copy(value.strip())

    def query(self, query):
        results = []
        # Mojang API doesn't allow checking UID for UID, skip if given query is already UID
        if len(query) < 32:
            r = requests.get(
                "https://api.mojang.com/users/profiles/minecraft/" + query)
            uid = r.json()["id"]
        else:
            uid = query
        # Requesting Namehistory from Mojang API using prior requested UID or given UID from query
        r = requests.get(
            "https://api.mojang.com/user/profiles/" + uid + "/names")
        result = r.json()

        pathToImage = "cache/" + uid + ".png"

        if not path.exists(pathToImage):
            urllib.request.urlretrieve(
                "https://minotar.net/helm/" + uid, pathToImage)

        for name in result:
            subTitle = ""
            if "changedToAt" not in name:
                subTitle = "Original Name"
            else:
                subTitle = time.strftime(
                    "%Y-%m-%d | %H:%M", time.localtime(int(name['changedToAt']) / 1000))
            results.insert(0, {
                "Title": name['name'],
                "SubTitle": subTitle,
                "IcoPath": pathToImage,
                "ContextData": name['name'],
                "JsonRPCAction": {
                    "method": "copyToClipboard",
                    "parameters": [uid],
                    "dontHideAfterAction": False
                }
            })

        return results

    def context_menu(self, data):
        results = []
        results.append({
            "Title": data,
            "SubTitle": "Copy Name",
            "IcoPath": "empty.png",
            "JsonRPCAction": {
                "method": "copyToClipboard",
                "parameters": [data],
                "dontHideAfterAction": False
            }
        })
        return results


if __name__ == "__main__":
    HelloWorld()
