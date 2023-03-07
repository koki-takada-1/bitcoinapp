import numpy as np
import pandas as pd
import datetime
import pandas_datareader.data as pdr
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests
import io
import plotly.express as px
import tkinter as tk
import webbrowser


dateend = datetime.date.today()
datestart = dateend - datetime.timedelta(days=15)
tickerlist = ["DEXJPUS"]

FREDdf = pdr.DataReader(tickerlist, "fred", datestart, dateend)  # 日次データ
FREDdf.columns = ["USD/JPY"]
for i in FREDdf.index:
    FREDdf = FREDdf.rename(index={i: str(i)[5:10]})

fig = plt.Figure(figsize=(6, 4))
ax1 = fig.add_subplot()
ax1.plot(FREDdf.index, FREDdf["USD/JPY"])
ax1.set_title("USD/JPY")
ax1.set_ylabel("JPY")


url_1 = "https://api.blockchain.info/charts/market-price?format=csv"
res = requests.get(url_1)

df = pd.read_csv(io.BytesIO(res.content), sep=",")
df.columns = ["time", "USD"]
for i, v in enumerate(df["time"]):
    df.iloc[i : i + 1, 0:1] = v[5:10]

fig2 = plt.Figure(figsize=(6, 4))
ax1 = fig2.add_subplot()
ax1.plot(df["time"], df["USD"])
ax1.set_xticks(df["time"][::120])
ax1.set_title("BTC/USD")
ax1.set_ylabel("USD")


def chart1():
    url = "https://api.blockchain.info/charts/market-price?format=csv"
    res = requests.get(url)

    df = pd.read_csv(io.BytesIO(res.content), sep=",")
    df.columns = ["date", "USD"]
    fig = px.line(df, x="date", y="USD")
    fig.show()


def chart2():
    url = "https://api.blockchain.info/charts/difficulty?format=csv"
    res = requests.get(url)
    df2 = pd.read_csv(io.BytesIO(res.content), sep=",")
    df2.columns = ["date", "Difficulty"]
    fig = px.line(df2, x="date", y="Difficulty")
    fig.show()


def chart3():
    url = "https://api.blockchain.info/charts/hash-rate?format=csv"
    res = requests.get(url)
    df3 = pd.read_csv(io.BytesIO(res.content), sep=",")
    df3.columns = ["date", "Total Hash Rate(TH/s)"]
    fig = px.line(df3, x="date", y="Total Hash Rate(TH/s)")
    fig.show()


url_2 = "https://chainflyer.bitflyer.com/v1/block/latest"
res = requests.get(url_2)
data_1 = res.json()

url_3 = "https://api.blockchain.info/stats"
res = requests.get(url_3)
data_2 = res.json()

height = data_1["height"]
halflife = height // 210000
last_halflife = 210000 * halflife

minutes_between = data_2["minutes_between_blocks"]
all_minutes = (last_halflife + 210000 - height) * 10  # 10分
day = all_minutes // 1140
hour = (all_minutes % 1140) // 60
minute = (all_minutes % 1140) % 60


dt1 = datetime.datetime.now()
pre = dt1 + datetime.timedelta(days=day, hours=hour, minutes=minute)
print(f"直近のブロック生成時間{minutes_between}")
print(f"ブロックの高さ{height}")
print(f"前回の半減期ブロック数{last_halflife}")
print(f"次の半減期までの残りブロック数{last_halflife+210000-height}")
print(f"次の半減期予想時間{pre.year}年{pre.month}月{pre.month}日{pre.month}時{pre.minute}分")


def _destroyWindow():
    root.quit()
    root.destroy()


def github_open():
    webbrowser.open("https://github.com/bitcoin", new=0, autoraise=True)


def bitcoin_org():
    webbrowser.open("https://bitcoin.org/ja/", new=0, autoraise=True)


def developer_guides():
    webbrowser.open(
        "https://developer.bitcoin.org/devguide/index.html",
        new=0,
        autoraise=True,
    )


def whitepaper():
    webbrowser.open("https://bitcoin.org/bitcoin.pdf")
    webbrowser.open("https://bitcoin.org/files/bitcoin-paper/bitcoin_jp.pdf")


root = tk.Tk()
root.title("ビットコインダッシュボード")
root.geometry("1280x720")
root.withdraw()
root.protocol(
    "WM_DELETE_WINDOW", _destroyWindow
)  # When you close the tkinter window.
men = tk.Menu(root)
root.config(menu=men)
men.add_command(label="github", command=github_open)
men.add_command(label="bitcoin.org", command=bitcoin_org)
men.add_command(label="開発者用ガイド", command=developer_guides)
men.add_command(label="原論文", command=whitepaper)

label1 = tk.Label(
    text=f"直近のブロック生成時間= {minutes_between}",
    foreground="orange",
    background="black",
    font=("MSゴシック", "20", "bold"),
)
label2 = tk.Label(
    text=f"ブロックの高さ= {height}",
    foreground="orange",
    background="black",
    font=("MSゴシック", "20", "bold"),
)
label3 = tk.Label(
    text=f"前回の半減期ブロック数= {last_halflife}",
    foreground="orange",
    background="black",
    font=("MSゴシック", "20", "bold"),
)
label4 = tk.Label(
    text=f"次の半減期までの残りブロック数= {last_halflife+210000-height}",
    foreground="orange",
    background="black",
    font=("MSゴシック", "20", "bold"),
)
label5 = tk.Label(
    text=f"次の半減期予想時間= {pre.year}年{pre.month}月{pre.month}日{pre.month}時{pre.minute}分",
    foreground="orange",
    background="black",
    font=("MSゴシック", "20", "bold"),
)
label6 = tk.Label(
    text=f"現在時刻：{datetime.datetime.now()}",
    foreground="orange",
    background="black",
    font=("MSゴシック", 22, "bold"),
)

label1.grid(row=1, column=0, sticky=tk.W)
label2.grid(row=2, column=0, sticky=tk.W)
label3.grid(row=3, column=0, sticky=tk.W)
label4.grid(row=4, column=0, sticky=tk.SW)
label5.grid(row=5, column=0, sticky=tk.SW)
label6.grid(row=10, column=0, columnspan=3, sticky=tk.SE)

hash_rate = data_2["hash_rate"]
difficulty = data_2["difficulty"]
market_price_usd = data_2["market_price_usd"]


# Canvas
canvas = FigureCanvasTkAgg(
    fig, master=root
)  # Generate canvas instance, Embedding fig in root
canvas.draw()
canvas.get_tk_widget().grid(row=0, column=0, sticky=tk.NW)
# canvas._tkcanvas.pack()
canvas = FigureCanvasTkAgg(
    fig2, master=root
)  # Generate canvas instance, Embedding fig in root
canvas.draw()
canvas.get_tk_widget().grid(row=0, column=1, sticky=tk.NE)
button1 = tk.Button(
    root,
    text=f"ハッシュレート= {hash_rate}",
    font=("MSゴシック", 20, "bold"),
    command=chart3,
)
button2 = tk.Button(
    root,
    text=f"採掘難易度(Difficulty)= {difficulty}",
    font=("MSゴシック", 20, "bold"),
    command=chart2,
)
button3 = tk.Button(
    root,
    text=f"BTC/USD＝ {market_price_usd}",
    font=("MSゴシック", 20, "bold"),
    command=chart1,
)

button1.grid(row=1, column=1, sticky=tk.E)
button2.grid(row=2, column=1, sticky=tk.E)
button3.grid(row=3, column=1, sticky=tk.SE)


# root
root.update()
root.deiconify()
root.mainloop()
