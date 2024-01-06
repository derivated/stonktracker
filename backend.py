import time
import requests
import json
import asyncio
import os
import datetime as dt
import matplotlib

loop = True
data = {}

if not os.path.isfile("data.json"):
    f = open("data.json", "x")
    f.write('{"data": {"sellPrice": {}, "buyPrice": {}, "sellMovingWeek": {}, "buyMovingWeek": {}}}')
    data = json.loads('{"data": {"sellPrice": {}, "buyPrice": {}, "sellMovingWeek": {}, "buyMovingWeek": {}}}')
    f.close()
else:
    f = open("data.json", "r")
    data = json.loads(f.read())
    f.close()
def get_data():
    url = "https://api.hypixel.net/v2/skyblock/bazaar"
    response = requests.get(url).json()
    return response


async def main():
    while loop:
        newData = get_data()
        timestamp = str(int(time.mktime(dt.datetime.now(dt.timezone.utc).timetuple())))
        data["data"]["sellPrice"][timestamp] = newData["products"]["STOCK_OF_STONKS"]["quick_status"]["sellPrice"]
        data["data"]["buyPrice"][timestamp] = newData["products"]["STOCK_OF_STONKS"]["quick_status"]["buyPrice"]
        data["data"]["sellMovingWeek"][timestamp] = newData["products"]["STOCK_OF_STONKS"]["quick_status"]["sellMovingWeek"]
        data["data"]["buyMovingWeek"][timestamp] = newData["products"]["STOCK_OF_STONKS"]["quick_status"]["buyMovingWeek"]


        f = open("data.json", "w")
        f.write(str(data))
        f.close()

        print("New Data Added")
        await asyncio.sleep(60)

asyncio.run(main())
