from selenium import webdriver
import pandas as pd
import os.path

# scrape stock names based on filters on Finviz
class StockList:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.tickers = []
        self.allSymbols = []

    def driverStart(self):
        #filter all stocks with average volume over 200k, change to desired filters and replace link
        tmp = 0
        while tmp <= 4501:
            url = "https://finviz.com/screener.ashx?v=111&f=sh_avgvol_o200&r={0}".format(tmp)
            self.driver.get(url)
            self.driver.implicitly_wait(7)
            self.getTickers()
            tmp = tmp + 20
    
    def writeTickersToCSV(self):
        if not os.path.isfile('./tickers.csv'):
            df = pd.DataFrame({'Symbol': self.tickers})
            df.to_csv('./tickers.csv')


    # scrape ticker name
    def getTickers(self):
        symbs = self.driver.find_elements_by_class_name("screener-link-primary")
        symbs = [i.text for i in symbs]
        # symbs = [i for i in symbs if i in self.allSymbols]
        symbs = list(dict.fromkeys(symbs))
        symbs = [i for i in symbs if i not in self.tickers]
        print(symbs)
        self.tickers.extend(symbs)
        print(len(self.tickers))

    # optional: check filtered stocks against certain exchanges
    def getAllStockSymbols(self):
        if os.path.isfile('./allSymbols.csv'):
            data = pd.read_csv("./allSymbols.csv")
            data = list(data.Symbol)
            self.allSymbols = data
        else:
            data = pd.read_csv("~/Downloads/nasdaq.csv")
            data = list(data.Symbol)
            self.allSymbols.extend(data)

            data = pd.read_csv("~/Downloads/amex.csv")
            data = list(data.Symbol)
            self.allSymbols.extend(data)

            data = pd.read_csv("~/Downloads/nyse.csv")
            data = list(data.Symbol)
            self.allSymbols.extend(data)

            df = pd.DataFrame({"Symbol": self.allSymbols})
            df.to_csv("./allSymbols.csv")


test = StockList()
# test.getAllStockSymbols()
test.driverStart()
test.writeTickersToCSV()
