import datetime
import io
import tkinter as tk
import webbrowser

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader.data as pdr
import plotly.express as px
import requests
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def main():
    root = tk.Tk()
    app = Application(root)
    app.mainloop()

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        # ウィンドウの設定
        master.title("ビットコインダッシュボード")
        master.geometry("1280x720")
        # 実行内容
        # メインフレームを配置
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        # APIから情報取得
        url_1 = "https://chainflyer.bitflyer.com/v1/block/latest"
        res = requests.get(url_1)
        data_1 = res.json()

        url_2 = "https://api.blockchain.info/stats"
        res = requests.get(url_2)
        data_2 = res.json()

        self.height = data_1["height"]
        halflife = self.height // 210000
        self.last_halflife = 210000 * halflife

        self.minute_between = data_2["minutes_between_blocks"]
        all_minutes = (self.last_halflife + 210000 - self.height) * 10  # 10分
        self.day = all_minutes // 1140
        self.hour = (all_minutes % 1140) // 60
        self.minute = (all_minutes % 1140) % 60

        self.hash_rate = data_2["hash_rate"]
        self.difficulty = data_2["difficulty"]
        self.market_price_usd = data_2["market_price_usd"]

        # メニューバー設定
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        menu.add_command(label="github", command=self.github_open)
        menu.add_command(label="bitcoin.org", command=self.bitcoin_org)
        menu.add_command(label="開発者用ガイド", command=self.developer_guides)
        menu.add_command(label="原論文", command=self.whitepaper)

        # チャート表示
        self.usd_yen(self.master)
        self.usd_btc(self.master)

        # ビットコイン情報ラベル表示
        self.information_labels()
        self.chart_button(self.master)

        # 1秒後に再度呼び出す
        self.after(1000, self.create_widgets)

    def github_open(self):
        webbrowser.open("https://github.com/bitcoin", autoraise=True)

    def bitcoin_org(self):
        webbrowser.open("https://bitcoin.org/ja/", autoraise=True)

    def developer_guides(self):
        webbrowser.open(
            "https://developer.bitcoin.org/devguide/index.html", autoraise=True
        )

    def whitepaper(self):
        webbrowser.open("https://bitcoin.org/bitcoin.pdf")
        webbrowser.open(
            "https://bitcoin.org/files/bitcoin-paper/bitcoin_jp.pdf"
        )

    def usd_yen(self, master):
        dateend = datetime.date.today()
        datestart = dateend - datetime.timedelta(days=15)
        tickerlist = ["DEXJPUS"]
        FREDdf = pdr.DataReader(
            tickerlist, "fred", datestart, dateend
        )  # 日次データ
        FREDdf.columns = ["USD/JPY"]
        for i in FREDdf.index:
            FREDdf = FREDdf.rename(index={i: str(i)[5:10]})
        fig = plt.Figure(figsize=(6, 4))
        ax1 = fig.add_subplot()
        ax1.plot(FREDdf.index, FREDdf["USD/JPY"])
        ax1.set_title("USD/JPY")
        ax1.set_ylabel("JPY")
        canvas = FigureCanvasTkAgg(
            fig, master=master
        )  # Generate canvas instance, Embedding fig in root
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky=tk.NW)

    def usd_btc(self, master):
        url = "https://api.blockchain.info/charts/market-price?format=csv"
        res = requests.get(url)

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
        canvas = FigureCanvasTkAgg(
            fig2, master=master
        )  # Generate canvas instance, Embedding fig in root
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=1, sticky=tk.NE)

    def information_labels(self):
        # ラベル作成
        dt1 = datetime.datetime.now()
        pre = dt1 + datetime.timedelta(
            days=self.day, hours=self.hour, minutes=self.minute
        )

        label1 = tk.Label(
            text=f"直近のブロック生成時間= {self.minute_between}",
            foreground="orange",
            background="black",
            font=("MSゴシック", "20", "bold"),
        )
        label2 = tk.Label(
            text=f"ブロックの高さ= {self.height}",
            foreground="orange",
            background="black",
            font=("MSゴシック", "20", "bold"),
        )
        label3 = tk.Label(
            text=f"前回の半減期ブロック数= {self.last_halflife}",
            foreground="orange",
            background="black",
            font=("MSゴシック", "20", "bold"),
        )
        label4 = tk.Label(
            text=f"次の半減期までの残りブロック数= {self.last_halflife+210000-self.height}",
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

    def chart_button(self, master):
        button1 = tk.Button(
            master,
            text=f"ハッシュレート= {self.hash_rate}",
            font=("MSゴシック", 20, "bold"),
            command=self.chart3,
        )
        button2 = tk.Button(
            master,
            text=f"採掘難易度(Difficulty)= {self.difficulty}",
            font=("MSゴシック", 20, "bold"),
            command=self.chart2,
        )
        button3 = tk.Button(
            master,
            text=f"BTC/USD＝ {self.market_price_usd}",
            font=("MSゴシック", 20, "bold"),
            command=self.chart1,
        )

        button1.grid(row=1, column=1, sticky=tk.E)
        button2.grid(row=2, column=1, sticky=tk.E)
        button3.grid(row=3, column=1, sticky=tk.SE)

    def chart1(self):
        url = "https://api.blockchain.info/charts/market-price?format=csv"
        res = requests.get(url)

        df = pd.read_csv(io.BytesIO(res.content), sep=",")
        df.columns = ["date", "USD"]
        fig = px.line(df, x="date", y="USD")
        fig.show()

    def chart2(self):
        url = "https://api.blockchain.info/charts/difficulty?format=csv"
        res = requests.get(url)
        df2 = pd.read_csv(io.BytesIO(res.content), sep=",")
        df2.columns = ["date", "Difficulty"]
        fig = px.line(df2, x="date", y="Difficulty")
        fig.show()

    def chart3(self):
        url = "https://api.blockchain.info/charts/hash-rate?format=csv"
        res = requests.get(url)
        df3 = pd.read_csv(io.BytesIO(res.content), sep=",")
        df3.columns = ["date", "Total Hash Rate(TH/s)"]
        fig = px.line(df3, x="date", y="Total Hash Rate(TH/s)")
        fig.show()


if __name__ == "__main__":
    main()
