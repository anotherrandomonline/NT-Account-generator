import random
import string
import threading
import requests
import config

def getproxies():
    proxies = []
    links = [
        "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/socks5_proxies.txt"

    ]
    for url in links:
        res = requests.get(url)
        if res.status_code == 200:
            for proxy in res.text.splitlines():
                proxies.append(proxy)

    print(f"Got {len(proxies)} proxies")
    return proxies

class NT:
    def __init__(self, proxy):
        self.session = requests.Session()
        proxy_link = f"socks5://{proxy}"
        self.session.proxies = {"http": proxy_link, "https": proxy_link}
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }
        
    def create_account(self):
        self.username = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(14, 20))).lower()
        self.password = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(14, 20)))

        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "referrer": "https://www.nitrotype.com/race",
        }

        data = {
            "username": f"{self.username}",
            "password": f"{self.password}",
            "acceptPolicy": "on",
            "receiveContact": "",
            "tz": "",
            "qualifying": 1,
            "avgSpeed": random.randint(200, 250),
            "avgAcc": 100,
            "carID": 9,
            "raceSounds": "only_fx"
        }

        try:
            register_res = self.session.post("https://www.nitrotype.com/api/v2/auth/register/username", json=data, headers=headers, timeout=10)
            if register_res.status_code == 200:
                with open("accounts.txt", "a") as file:
                    file.write(f"{self.username}:{self.password}\n")

                print("Created account")

                self.token = register_res.json()["results"]["token"]
                self.uid = register_res.json()["results"]["userID"]

                self.display_name()
                if config.FRIEND_SPAM: self.friend()
                if config.JOIN_TEAM: self.join_team()

        except: print("Failed to create account")

    def display_name(self):
        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "authorization": f"Bearer {self.token}",
            "referrer": "https://www.nitrotype.com/profile",
            "x-uid": str(self.uid)
        }
        data = {
            "displayName": config.NAME,
            "password": self.password
        }
        try:
            self.session.post("https://www.nitrotype.com/api/v2/settings/profile", headers=headers, json=data, timeout=10)
        except: pass

    def join_team(self):
        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "authorization": f"Bearer {self.token}",
            "referrer": "https://www.nitrotype.com/team",
            "x-uid": str(self.uid)
        }
        for team in config.TEAMS:
            try:
                self.session.post(f"https://www.nitrotype.com/api/v2/teams/{team}/apply", headers=headers, timeout=10)
            except: pass

    def friend(self):
        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "authorization": f"Bearer {self.token}",
            "referrer": "https://www.nitrotype.com/racer/",
            "x-uid": str(self.uid)
        }
        for racer in config.FRIEND:
            try:
                self.session.post(f"https://www.nitrotype.com/api/v2/friend-requests/{racer}/request", headers=headers, timeout=10)
            except: pass

    def start(self):
        threading.Thread(target=self.create_account).start()
