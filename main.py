import random
import time

import API

proxies = API.getproxies()

while True:
    proxy = random.choice(proxies)
    api = API.NT(proxy)
    api.start()
    time.sleep(.05)