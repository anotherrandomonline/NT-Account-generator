import random
import string
import threading
import requests

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
        username = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(14, 20))).lower()
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(14, 20)))

        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "referrer": "https://www.nitrotype.com/race",
        }
        data = {
            "username": f"{username}",
            "password": f"{password}",
            "acceptPolicy": "on",
            "receiveContact": "",
            "tz": "",
            "qualifying": 1,
            "avgSpeed": 250,
            "avgAcc": 100,
            "carID": 9,
            "raceSounds": "only_fx"
        }
        try:
            register_res = self.session.post("https://www.nitrotype.com/api/v2/auth/register/username", json=data, headers=headers, timeout=10)
            if register_res.status_code == 200:
                with open("accounts.txt", "a") as file:
                    file.write(f"{username}:{password}\n")
                print("Created account")
        except: print("Failed to create account")

    def start(self):
        threading.Thread(target=self.create_account).start()
