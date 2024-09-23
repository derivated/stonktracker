import time
import requests
import json
import asyncio
import os
import datetime as dt
import pytz as tz

loop = True
data = {}
historicData = {}
summaryData = {}

if not os.path.isfile("data.json"):
    f = open("data.json", "x")
    f.write('{"data": {"sellPrice": {}, "buyPrice": {}, "sellMovingWeek": {}, "buyMovingWeek": {}}}')
    data = json.loads('{"data": {"sellPrice": {}, "buyPrice": {}, "sellMovingWeek": {}, "buyMovingWeek": {}}}')
    f.close()
else:
    f = open("data.json", "r")
    data = json.loads(f.read())
    f.close()

if not os.path.isfile("historic_data.json"):
    f = open("historic_data.json", "x")
    f.write(str(data).replace("'", '"'))
    historicData = data
    f.close()
else:
    f = open("historic_data.json", "r")
    historicData = json.loads(f.read())
    f.close()

if not os.path.isfile("summary.json"):
    f = open("summary.json", "x")
    f.write('{"data": {"sellSummary": {}, "buySummary": {}}}')
    summaryData = json.loads('{"data": {"sellSummary": {}, "buySummary": {}}}')
    f.close()
else:
    f = open("summary.json", "r")
    summaryData = json.loads(f.read())
    f.close()


def get_data():
    url = "https://api.hypixel.net/v2/skyblock/bazaar"
    response = requests.get(url).json()
    return response


async def main():
    global data
    global historicData
    global summaryData
    while loop:
        newData = get_data()
        timestamp = str(int(time.mktime(dt.datetime.now(tz.timezone('America/Los_Angeles')).timetuple())))
        data["data"]["sellPrice"][timestamp] = newData["products"]["BOOSTER_COOKIE"]["quick_status"]["sellPrice"]
        data["data"]["buyPrice"][timestamp] = newData["products"]["BOOSTER_COOKIE"]["quick_status"]["buyPrice"]
        data["data"]["sellMovingWeek"][timestamp] = newData["products"]["BOOSTER_COOKIE"]["quick_status"]["sellMovingWeek"]
        data["data"]["buyMovingWeek"][timestamp] = newData["products"]["BOOSTER_COOKIE"]["quick_status"]["buyMovingWeek"]

        for i in range(10):
            try:
                summaryData["data"]["sellSummary"][str(i + 1)] = newData["products"]["BOOSTER_COOKIE"]["sell_summary"][i]
                summaryData["data"]["buySummary"][str(i + 1)] = newData["products"]["BOOSTER_COOKIE"]["buy_summary"][i]
            except:
                break

        f = open("data.json", "w")
        f.write(str(data).replace("'", '"'))
        f.close()

        f = open("historic_data.json", "r")
        historicData = json.loads(f.read())
        f.close()

        historicData["data"]["sellPrice"][timestamp] = data["data"]["sellPrice"][timestamp]
        historicData["data"]["buyPrice"][timestamp] = data["data"]["buyPrice"][timestamp]
        historicData["data"]["sellMovingWeek"][timestamp] = data["data"]["sellMovingWeek"][timestamp]
        historicData["data"]["buyMovingWeek"][timestamp] = data["data"]["buyMovingWeek"][timestamp]


        prev = 0
        toDelete = []
        for i in historicData["data"]["sellPrice"]:
            if int(i) >= prev + 3600:
                prev = int(i)
            else:
                toDelete.append(i)

        for i in toDelete:
            del historicData["data"]["sellPrice"][i]
            del historicData["data"]["buyPrice"][i]
            del historicData["data"]["sellMovingWeek"][i]
            del historicData["data"]["buyMovingWeek"][i]

        f = open("historic_data.json", "w")
        f.write(str(historicData).replace("'", '"'))
        f.close()

        toDelete = []
        for i in data["data"]["sellPrice"]:
            if int(i) < int(timestamp) - 86400:
                toDelete.append(i)

        for i in toDelete:
            del data["data"]["sellPrice"][i]
            del data["data"]["buyPrice"][i]
            del data["data"]["sellMovingWeek"][i]
            del data["data"]["buyMovingWeek"][i]

        f = open("summary.json", "w")
        f.write(str(summaryData).replace("'", '"'))
        f.close()

        print("New Data Added")
        await asyncio.sleep(60)

asyncio.run(main())
