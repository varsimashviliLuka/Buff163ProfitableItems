# Hello everyone! This program helps you to find profitable items on Buff163
# Hope you like it!
# Importing libraries that I need
from flask import Flask, render_template
import json
import requests

# Here I am creating class for Skin and defining it's parameters, also creating functions to calculate it's profits and
# Percents
class Skin:
    def __init__(self,name,sellPrice,buyPrice,img,link,id,sellNum):
        self.name=name
        self.sellPrice=float(sellPrice)
        self.buyPrice=float(buyPrice)
        self.img=img
        self.link=link
        self.id=id
        self.sellNum=int(sellNum)

    def calculateProfit(self):
        profit = float(self.sellPrice*0.975-self.buyPrice)
        return profit

    def calculatePercent(self):
        percent = float(self.calculateProfit()/self.buyPrice)
        return percent

# Here I am creating 2 functions to return rounded number (It is easier to pass it to html)
    def calculateProfitShort(self):
        profit = round(self.calculateProfit(),3)
        return float(profit)

    def calculatePercentShort(self):
        percent = round(self.calculatePercent(),3)
        return float(percent)

# I created this function to compare old config and new config, if there is differance page number (count) turns into 0 to start from 0
def readConfig():
    with open("config.txt","r") as f:
        return f.read()

oldConfig = readConfig()

app = Flask(__name__)
count = 0

@app.route('/')
def index():
    global count
    global oldConfig
    config = readConfig()

    if config != oldConfig:
        oldConfig = config
        count = 0
    with open("config.txt","r") as f:
        configJ = json.load(f)

    COOKIES = configJ["cookies"]
    MINPRICE = configJ["prices"]["minPrice"]
    MAXPRICE = configJ["prices"]["maxPrice"]
    ALLOWEDPERCENT = configJ["prices"]["allowedPercent"]

    count += 1
    LINK = f"https://buff.163.com/api/market/goods?game=csgo&page_num={count}&page_size=100&min_price={MINPRICE}&max_price={MAXPRICE}&sort_by=price.asc"
    r = requests.get(LINK, cookies=COOKIES).json()
    itemsUnfiltered = r["data"]["items"]
    items = []

    for item in itemsUnfiltered:
        name = item["market_hash_name"]
        sellPrice = item["sell_min_price"]
        buyPrice = item["buy_max_price"]
        img = item["goods_info"]["icon_url"]
        id = item["id"]
        sellNum = item["sell_num"]
        link = f"https://buff.163.com/goods/{id}?from=market"

        skin = Skin(name,sellPrice,buyPrice,img,link,id,sellNum)

        if skin.sellNum >= 90 and skin.sellNum <= 700:
            if skin.calculatePercent() >= ALLOWEDPERCENT:
                items.append(skin)
    return render_template('index.html', items=items)

if __name__ == "__main__":
    app.run()


# L.Varsimashvili :)
