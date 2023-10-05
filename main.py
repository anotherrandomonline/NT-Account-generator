import random
import time

import API
import config

if len(config.NAME) > 20 or len(config.NAME) < 6:
    print("config.NAME must be between 6 and 20 characters")
    exit(0)

proxies = API.getproxies()

while True:
    proxy = random.choice(proxies)
    api = API.NT(proxy)
    api.start()
    time.sleep(.05)