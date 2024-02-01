from flask import Flask, render_template, request, send_file
app = Flask(__name__)
import cloudscraper
import numpy
import datetime
import yfinance as yf
from tabulate import tabulate
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import traceback,threading
import matplotlib.pyplot as plt
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from PIL import Image
from io import BytesIO

date_format = "%Y-%m-%d"
requests = cloudscraper.Session()
def is_integer(s):
    try:
        int(s)
        return False
    except ValueError:
        return True
def calculate_annual_return(ticker):
  # Fetch historical data
  end_date = datetime.now()
  start_date = end_date - timedelta(days=Years * 365)
  data = yf.download(ticker, start=start_date, end=end_date, session=requests)
  if len(data) < 0.9 * (Years * 365 - (113.8 * Years)):
    return False
  annual_returns = (data['Adj Close'].pct_change() +
                    1).resample('Y').prod() - 1
  average_annual_return = annual_returns.mean()
  data['Daily_Return'] = data['Adj Close'].pct_change()
  data['Cumulative_Return'] = (1 + data['Daily_Return']).cumprod()
  data['Cumulative_Max'] = data['Cumulative_Return'].cummax()
  data['Drawdown'] = data['Cumulative_Return'] / data['Cumulative_Max'] - 1
  max_drawdown = data['Drawdown'].min()
  daily_returns = data['Adj Close'].pct_change().dropna()
  volatility = daily_returns.std()
  ProfitStock = True if max_drawdown >= (MaxDrawDown -
                                         MaxDrawDown * 2) / 100 else False
  return ProfitStock
class General():
    def StockGrabber():
        global StockDataLen
        StockData1 = requests.post("https://scanner.tradingview.com/america/scan",json={"columns":["name","close","Perf.1M","Perf.3M","Perf.6M","Perf.Y","Perf.5Y","Perf.All","price_earnings_ttm"],"ignore_unknown_fields":False,"options":{"lang":"en"},"range":[0,1000000],"sort":{"sortBy":"name","sortOrder":"asc","nullsFirst":False},"preset":"all_stocks"}).json()
        StockData2 = requests.post("https://scanner.tradingview.com/japan/scan",json={"columns":["name","close","Perf.1M","Perf.3M","Perf.6M","Perf.Y","Perf.5Y","Perf.All","price_earnings_ttm"],"ignore_unknown_fields":False,"options":{"lang":"en"},"range":[0,1000000],"sort":{"sortBy":"name","sortOrder":"asc","nullsFirst":False},"preset":"all_stocks"}).json()
        StockData3 = requests.post("https://scanner.tradingview.com/korea/scan",json={"columns":["name","close","Perf.1M","Perf.3M","Perf.6M","Perf.Y","Perf.5Y","Perf.All","price_earnings_ttm"],"ignore_unknown_fields":False,"options":{"lang":"en"},"range":[0,1000000],"sort":{"sortBy":"name","sortOrder":"asc","nullsFirst":False},"preset":"all_stocks"}).json()
        StockData4 = requests.post("https://scanner.tradingview.com/germany/scan",json={"columns":["name","close","Perf.1M","Perf.3M","Perf.6M","Perf.Y","Perf.5Y","Perf.All","price_earnings_ttm"],"ignore_unknown_fields":False,"options":{"lang":"en"},"range":[0,1000000],"sort":{"sortBy":"name","sortOrder":"asc","nullsFirst":False},"preset":"all_stocks"}).json()
        StockData5 = requests.post("https://scanner.tradingview.com/uk/scan",json={"columns":["name","close","Perf.1M","Perf.3M","Perf.6M","Perf.Y","Perf.5Y","Perf.All","price_earnings_ttm"],"ignore_unknown_fields":False,"options":{"lang":"en"},"range":[0,1000000],"sort":{"sortBy":"name","sortOrder":"asc","nullsFirst":False},"preset":"all_stocks"}).json()
        StockData = []
        for Data in StockData1["data"]:
            StockData.append(Data)
        for Data in StockData2["data"]:
            StockData.append(Data)
        for Data in StockData3["data"]:
            StockData.append(Data)
        for Data in StockData4["data"]:
            StockData.append(Data)
        for Data in StockData5["data"]:
            StockData.append(Data)
        StockDataLen = len(StockData)
        return numpy.array(StockData)
    
    def Main(YearsGiven,MaxDrawDownGiven,Years5ProfitGiven,Year1ProfitGiven,MinimumPriceGiven):
        global Years, MaxDrawDown, Years5Profit, Year1Profit, MinimumPrice
        Years, MaxDrawDown, Years5Profit, Year1Profit, MinimumPrice = YearsGiven,MaxDrawDownGiven, Years5ProfitGiven,Year1ProfitGiven,MinimumPriceGiven
        return ProcessData.CalculateData()

class ProcessData():
    def ConvertData(StockData):
        Data = {}
        for GetVal in StockData:
            Data[GetVal["d"][0]] = [GetVal["d"][1],GetVal["d"][2],GetVal["d"][3],GetVal["d"][4],GetVal["d"][5],GetVal["d"][6],GetVal["d"][7],GetVal["d"][8]]
        return Data
    def Add(Names):
        FinalStocks["Stock"].append(Names)
    def CalculateData():
        global FinalStocks
        FinalStocks = {"Stock": []}
        StockData = General.StockGrabber()
        Data = ProcessData.ConvertData(StockData)
        current_date = datetime.now()
        date_format = "%Y-%m-%d"
        some_years_ago = current_date - timedelta(days=365 * Years)
        NameData = []
        for Names in Data:
            if is_integer(Names):
                if (
                    Data[Names][5] > Years5Profit
                    and Data[Names][4] > Year1Profit
                    and Data[Names][0] > MinimumPrice
                ):
                    NameData.append(Names)
        stock_data = yf.download(
                            NameData,
                            start=some_years_ago,
                            end=current_date.strftime(date_format),
                            session=requests,
                        )
        DownloadedNames = stock_data["Adj Close"].columns
        for StockData in DownloadedNames:
            try:
                EPSGrowth = stock_data["Adj Close"][StockData] / stock_data["Adj Close"][StockData].shift(1) - 1
                if EPSGrowth.mean() > 0:
                    if calculate_annual_return(StockData):
                        print(f"{StockData}")
                        FinalStocks["Stock"].append(StockData)
            except:
                pass
        return FinalStocks["Stock"]

@app.route('/')
def index():
    return render_template("index.html")
@app.route('/Stocks', methods=["POST"])
def GetStocks():
    return General.Main(float(request.json["YearsToCheck"]),float(request.json["MaxDrawDown"]),float(request.json["FiveYearsProfit"]),float(request.json["OneYearProfit"]),float(request.json["YearsToCheck"]))
@app.route('/GetStockChart', methods=["POST"])
def GetStockChart():
    symbol = request.json["Symbol"]
    current_date = datetime.now()
    some_years_ago = current_date - timedelta(days=365 * 10)
    stock_data = yf.download(symbol, start=some_years_ago, end=current_date)

    # Plot stock data
    plt.figure(figsize=(10, 6))
    plt.plot(stock_data['Close'], label=f'{symbol} Closing Price')
    plt.title(f'{symbol} Stock Chart')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.legend()

    # Save plot as an image
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    return send_file(img_buffer, mimetype='image/png')
if __name__ == '__main__':
    app.run(host='0.0.0.0')
General.Main()
def get_stock_data(symbol, start_date, end_date):
    # Download historical data as a Pandas DataFrame
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    return stock_data
