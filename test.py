import pandas as pd
import pandas_datareader.data as web
import datetime

start = datetime.datetime(2018, 1, 1)
end = datetime.date.today()

#Read in and store data
fb = web.DataReader('FB', 'morningstar', start, end)

dates = []
prices = []
percents = [0]

#Initialize dates and prices with correlating indexes
for index, row in fb.iterrows():
    prices.append(row['Close'])
    dates.append(index[1].strftime('%m/%d/%y'))

i = 1
#Get daily percentage changes from data
while i < len(prices):
    today = prices[i]
    yesterday = prices[i-1]
    percent = (today-yesterday)/yesterday
    percents.append(round(percent*100,2))
    i += 1

print ""




#Simulate market
startingBalance = 1000
balance = startingBalance
inMarket = 0
profitCount = 0
lossCount = 0


i = 0
while i < len(percents):
    if percents[i] <= -2.5: #Invest when market drops 2.5%
        buyPrice = prices[i]
        shares = int(balance / buyPrice) 
        print dates[i],"\tBought", shares, "shares for $", buyPrice, "per share"
        j = i
        while j < len(prices):
            movePct = prices[j] / buyPrice
            if movePct > 1.05: #Cut gains at 5%
                profit = shares*prices[j] - shares*buyPrice
                profitCount += 1
                print dates[j], "\tSold", shares, "shares for $", prices[j], "per share"
                print "New account balance:", balance, "+", profit,"=", balance+profit
                balance += profit
                break
            elif movePct < 0.98: #Cut losses at -2%
                loss = shares*prices[j] - shares*buyPrice
                lossCount += 1
                print dates[j], "\tSold", shares, "shares for $", prices[j], "per share"
                print "New account balance:", balance, "-", loss * -1,"=", balance-loss
                balance -= loss
                break
            j += 1
        print ""
    i += 1

print "Starting balance:", startingBalance
print "Ending balance:", balance
print "Overall change:", (balance - startingBalance) / startingBalance * 100, "%"

#print "Profit count: ", profitCount
#print "Loss count: ", lossCount