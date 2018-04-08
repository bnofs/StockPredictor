import pandas as pd
import pandas_datareader.data as web
import datetime

start = datetime.datetime(2018, 1, 1)
end = datetime.date.today()

fb = web.DataReader('FB', 'morningstar', start, end)

prices = []
percents = [0]

for index, row in fb.iterrows():
    prices.append(row['Close'])

i = 1
while i < len(prices):
    today = prices[i]
    yesterday = prices[i-1]
    percent = (today-yesterday)/yesterday
    percents.append(round(percent*100,2))
    i += 1

balance = 5000
inMarket = 0
profitCount = 0
lossCount = 0

i = 0
while i < len(percents):
    if percents[i] <= -2.5: #Invest when market drops 2.5%
        buyPrice = prices[i]
        shares = int(1000 / buyPrice) 
        print "\nBought", shares, "shares for $", buyPrice, "per share"
        j = i
        while j < len(prices):
            movePct = prices[j] / buyPrice
            if movePct > 1.05: #Cut gains at 5%
                profit = shares*prices[j] - shares*buyPrice
                balance += profit
                profitCount += 1
                print "Sold for $", prices[j], "for profit of $", profit
                print "New account balance: ", balance
                break
            elif movePct < 0.98: #Cut losses at -2%
                loss = shares*prices[j] - shares*buyPrice
                balance -= loss
                lossCount += 1
                print "Sold for $", prices[j], "for loss of $", loss
                print "New account balance:", balance
                break
            j += 1
    i += 1

print "Profit count: ", profitCount
print "Loss count: ", lossCount