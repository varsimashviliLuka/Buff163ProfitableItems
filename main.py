from flask import Flask, render_template, request, session, redirect
import requests
import random

SECRET_KEY = random.randint(1000000000,9999999999)

app = Flask(__name__)
app.config['SECRET_KEY'] = str(SECRET_KEY)

class Item:
    def __init__(self, name, sellPrice, buyPrice, img, link, id, sellNum):
        self.name = name
        self.sellPrice = float(sellPrice)
        self.buyPrice = float(buyPrice)
        self.img = img
        self.link = link
        self.id = id
        self.sellNum = int(sellNum)
    def calculateProfit(self):
        return float(self.sellPrice * 0.975 - self.buyPrice)
    def calculatePercent(self):
        return float(self.calculateProfit() / self.buyPrice) * 100

@app.route('/<pageNum>', methods=['GET', 'POST'])
def main(pageNum):
    items = []
    session['pageNum'] = int(pageNum)
    if request.method == 'POST':
        items.clear()
        if request.form['cookies'] == "":
            pass
        else:
            session["cookies"] = request.form['cookies']
        if request.form['minPrice'] == "":
            pass
        else:
            session["minPrice"] = float(request.form['minPrice'])
        if request.form['maxPrice'] == "":
            pass
        else:
            session["maxPrice"] = request.form['maxPrice']
        if request.form['allowedPercent'] == "":
            pass
        else:
            session["allowedPercent"] = float(request.form['allowedPercent'])
        try:
            session["allowStickers"] = request.form.getlist('allowStickers')[0]
        except:
            session["allowStickers"] = 0
        try:
            session["allowSouvenirs"] = request.form.getlist('allowSouvenirs')[0]
        except:
            session["allowSouvenirs"] = 0
        session['pageNum'] = 1
        return redirect(f'/{session['pageNum']}')
    else:
        try:
            link = f"https://buff.163.com/api/market/goods?game=csgo&page_num={session['pageNum']}&page_size=100&min_price={session['minPrice']}&max_price={session['maxPrice']}&sort_by=price.asc"

            response = requests.get(link, cookies={"cookies": session['cookies']}).json()

            response = response['data']['items']
            for each in response:
                name = each["market_hash_name"]
                sellPrice = each["sell_min_price"]
                buyPrice = each["buy_max_price"]
                img = each["goods_info"]["icon_url"]
                link = f"https://buff.163.com/goods/{each['id']}?from=market"
                id = each["id"]
                sellNum = each["sell_num"]
                item = Item(name, sellPrice, buyPrice, img, link, id, sellNum)
                if item.calculatePercent() >= session["allowedPercent"]:
                    if item.sellNum >= 90 and item.sellNum <= 700:
                        if "Sticker" in item.name:
                            if str(session["allowStickers"]) == "1":
                                items.append(item)
                        elif "Souvenir" in item.name:
                            if str(session["allowSouvenirs"]) == "1":
                                items.append(item)
                        else:
                            items.append(item)
        except:
            pass
        return render_template("index.html",items=items)

@app.route('/')
def index():
    return redirect('/0')


if __name__ == '__main__':
    app.run()
