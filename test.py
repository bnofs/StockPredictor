import pandas as pd
import pandas_datareader.data as web
import datetime

#Stock class has a name, list of prices and list of percents
class Stock(object):
    name = ""
    prices = []
    percents = [0]
    def __init__(self, name, prices, percents):
        self.name = name
        self.prices = prices
        self.percents = percents

#Returns biggest loser in the market for the previous day
def biggestMarketLoser(stocks, index):
    minStock = stocks[0]
    i = 0
    while i < len(stocks):
        #print stocks[i].name, len(stocks[i].percents), index
        if stocks[i].percents[index] < minStock.percents[index]:
            minStock = stocks[i]
        i += 1
    #print minStock.name
    return minStock

start = datetime.datetime(2018, 1, 1)
end = datetime.date.today()

tickers = []
stocks = []
dates = []

#Get ticker symbols from txt file
with open('tickers.txt') as file:
  tickers = [i.strip() for i in file]
    
#For every stock in the list
for k in range(len(tickers)):
    print tickers[k]

    #Read in data and store
    temp = web.DataReader(tickers[k], 'morningstar', start, end)
    stock = Stock(tickers[k], [], [0])
    stocks.append(stock)

    #Initialize dates and prices with correlating indexes
    for index, row in temp.iterrows():
        stock.prices.append(row['Close'])
        if len(dates) < len(stock.prices):
            dates.append(index[1].strftime('%m/%d/%y'))

    #Get daily percentage changes from data
    i = 1
    while i < len(stock.prices):
        today = stock.prices[i]
        yesterday = stock.prices[i-1]
        percent = (today-yesterday)/yesterday
        stock.percents.append(round(percent*100,2))
        i += 1
    
print ""

#Simulate market
startingBalance = 1000
balance = startingBalance
inMarket = 0
profitCount = 0
lossCount = 0
stopGainPct = 1.05
stopLossPct = 0.98

i = 0
while i < len(dates):

    s = biggestMarketLoser(stocks, i)

    if s.percents[i] <= -2.5: #Invest when market drops 2.5%
        buyPrice = s.prices[i]
        shares = int(balance / buyPrice) 
        j = i
        while j < len(s.prices):
            movePct = s.prices[j] / buyPrice
            if movePct > stopGainPct: #Cut gains at 5%
                profit = shares*s.prices[j] - shares*buyPrice
                profitCount += 1
                print dates[i],"\tBought", shares, "shares of", s.name, "for $", buyPrice, "per share"
                print dates[j], "\tSold", shares, "shares of", s.name, "for $", s.prices[j], "per share"
                print "New account balance:", balance, "+", profit,"=", balance+profit
                balance += profit
                i = j
                break
            elif movePct < stopLossPct: #Cut losses at -2%
                loss = shares*s.prices[j] + shares*buyPrice
                lossCount += 1
                print dates[i],"\tBought", shares, "shares of", s.name, "for $", buyPrice, "per share"
                print dates[j], "\tSold", shares, "shares of", s.name, "for $", s.prices[j], "per share"
                print "New account balance:", balance, "-", loss,"=", balance-loss
                balance -= loss
                i = j
                break
            j += 1
        print ""
    i += 1
print "From",dates[0],"to",dates[len(dates)-1]
print "Stop gain percentage:",stopGainPct
print "Stop loss percentage:",stopLossPct
print "Starting balance:", startingBalance
print "Ending balance:", balance
print "Overall change:", (balance - startingBalance) / startingBalance * 100, "%"

print "Profit count: ", profitCount
print "Loss count: ", lossCount