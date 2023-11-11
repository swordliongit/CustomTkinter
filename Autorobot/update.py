import json
import subprocess
import sys
import requests
import zipfile

import os
from dotenv import load_dotenv
from packaging import version
from cryptography.fernet import Fernet

load_dotenv()

encryption_key = os.getenv("ENCRYPTION_KEY")
cipher_suite = Fernet(encryption_key.encode())


current_dir = os.path.dirname(__file__)


class Update:
    def __init__(self) -> None:
        self.session = requests.Session()

    def Login(self):
        """_summary_

        Args:
            session (requests.Session): _description_

        Returns:
            requests.Session: _description_
        """
        raw_data = {
            "jsonrpc": "2.0",
            "params": {
                "login": cipher_suite.decrypt(os.getenv("LOGIN").encode()).decode(),
                "password": cipher_suite.decrypt(os.getenv("PASSWORD").encode()).decode(),
                "db": cipher_suite.decrypt(os.getenv("DB").encode()).decode(),
            },
        }

        headers = {
            "content-type": "application/json",
        }

        payload = json.dumps(raw_data)
        response = self.session.post(url=cipher_suite.decrypt(os.getenv("URL_LOGIN").encode()).decode(), data=payload, headers=headers)
        # print(response.content)

    def Read(self):
        raw_data = {
            "id": 109,
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "model": cipher_suite.decrypt(os.getenv("MODEL").encode()).decode(),
                "method": cipher_suite.decrypt(os.getenv("METHOD").encode()).decode(),
                "args": [],
                "kwargs": {
                    "limit": 80,
                    "offset": 0,
                    "order": "",
                    "context": {"lang": "en_US", "tz": "Europe/Istanbul", "uid": 2, "allowed_company_ids": [1], "bin_size": True},
                    "count_limit": 10001,
                    "domain": [["name", "=", "Prototype"]],
                    "fields": ["name", "version", "push_update", "developer"],
                },
            },
        }

        headers = {
            "authority": "swordlion.org",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,tr;q=0.8",
            "content-type": "application/json",
            "origin": cipher_suite.decrypt(os.getenv("HEADERS_ORIGIN").encode()).decode(),
            "referer": cipher_suite.decrypt(os.getenv("HEADERS_REFERER").encode()).decode(),
            "sec-ch-ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        }

        payload = json.dumps(raw_data)
        response = self.session.post(url=cipher_suite.decrypt(os.getenv("URL_READ").encode()).decode(), data=payload, headers=headers)
        response_data = response.json()
        isUpdateAvailable = response_data["result"]["records"][0]["push_update"]
        version_cloud = response_data["result"]["records"][0]["version"]
        developer = response_data["result"]["records"][0]["developer"]
        version_current = ""
        with open(os.path.join(current_dir, ".version"), "r") as vfile:
            version_current = vfile.readline()
        if version.parse(version_current) < version.parse(version_cloud) and not developer:
            return isUpdateAvailable
        else:
            return False

    def IsUpdateAvailable(self) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        self.Login()
        return self.Read()

    def ApplyUpdate(self):
        """_summary_"""
        if self.DownloadUpdate():
            subprocess.Popen(["Autorobot_Updater.exe"])
            sys.exit()

    def DownloadUpdate(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Referer": cipher_suite.decrypt(os.getenv("HEADERS_REFERER").encode()).decode(),
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "TE": "trailers",
        }
        response = self.session.get(url=cipher_suite.decrypt(os.getenv("URL_UPDATE").encode()).decode(), headers=headers)
        # print(response.content)
        # Check if the request was successful
        if response.status_code == 200:
            # Save the downloaded file
            with open(os.path.join(current_dir, cipher_suite.decrypt(os.getenv("UPDATE_SAVE_PATH").encode()).decode()), "wb") as file:
                for chunk in response.iter_content(chunk_size=128):
                    file.write(chunk)
            return True
        else:
            print(f"Failed to download the update. Status code: {response.status_code}")
            return False


if __name__ == "__main__":
    pass
