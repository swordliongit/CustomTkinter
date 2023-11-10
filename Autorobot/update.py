import json
import requests

import os
from dotenv import load_dotenv

load_dotenv()


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
                "login": os.getenv("LOGIN"),
                "password": os.getenv("PASSWORD"),
                "db": os.getenv("DB"),
            },
        }

        headers = {
            "content-type": "application/json",
        }

        payload = json.dumps(raw_data)
        response = self.session.post(url=os.getenv("URL_Login"), data=payload, headers=headers)
        # print(response.content)

    def Read(self):
        raw_data = {
            "id": 109,
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "model": os.getenv("MODEL"),
                "method": os.getenv("METHOD"),
                "args": [],
                "kwargs": {
                    "limit": 80,
                    "offset": 0,
                    "order": "",
                    "context": {"lang": "en_US", "tz": "Europe/Istanbul", "uid": 2, "allowed_company_ids": [1], "bin_size": True},
                    "count_limit": 10001,
                    "domain": [["name", "=", "Prototype"]],
                    "fields": ["name", "version", "push_update"],
                },
            },
        }

        headers = {
            "authority": "swordlion.org",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,tr;q=0.8",
            "content-type": "application/json",
            "origin": os.getenv("HEADERS_ORIGIN"),
            "referer": os.getenv("HEADERS_REFERER"),
            "sec-ch-ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        }

        payload = json.dumps(raw_data)
        response = self.session.post(url=os.getenv("URL_READ"), data=payload, headers=headers)
        response_data = response.json()
        isUpdateAvailable = response_data["result"]["records"][0]["push_update"]
        return isUpdateAvailable

    def IsUpdateAvailable(self) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        self.Login()
        return self.Read()

    def ApplyUpdate(self):
        """_summary_"""
        self.DownloadUpdate()

    def DownloadUpdate(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Referer": os.getenv("HEADERS_REFERER"),
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "TE": "trailers",
        }
        response = self.session.get(url=os.getenv("URL_UPDATE"), headers=headers)
        # print(response.content)
        # Check if the request was successful
        if response.status_code == 200:
            # Save the downloaded file
            with open(os.path.abspath(os.path.join(os.getcwd(), os.getenv("UPDATE_SAVE_PATH"))), "wb") as file:
                for chunk in response.iter_content(chunk_size=128):
                    file.write(chunk)
        else:
            print(f"Failed to download the update. Status code: {response.status_code}")


if __name__ == "__main__":
    pass
