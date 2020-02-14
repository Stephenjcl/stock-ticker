from random import randint, choice
import time
import os
from math import floor
import re
#import matplotlib.pyplot as plt
#import matplotlib.ticker as tck
#import numpy as np


#settings = [line.rstrip('\n') for line in open("config.ini")]
#cash, players, turns_per_round, rounds = [int(settings[i].split("=")[1]) for i in range(4)]

cash = 5000
players = 8
turns_per_round = 7
rounds = 90
rolls = players*turns_per_round

stockdict = {
    "Oil" : 1.00,
    "Gold" : 1.00,
    "Silver" : 1.00,
    "Bonds" : 1.00,
    "Grain" : 1.00,
    "Industrial" : 1.00
}

owneddict = {
    "Oil" : 0,
    "Gold" : 0,
    "Silver" : 0,
    "Bonds" : 0,
    "Grain" : 0,
    "Industrial" : 0
}

shortdict = {
        "Oi" : "Oil",
        "Go" : "Gold",
        "Si" : "Silver",
        "Bo" : "Bonds",
        "Gr" : "Grain",
        "In" : "Industrial",
        }


def replace_str_index(text,index=0,replacement=''):
    return '%s%s%s'%(text[:index],replacement,text[index+1:])

def myround(x, base=500):
    return base * round(x/base)

def messages(d, m = None):
    if m == None:
        d = d[-5:]
        for elem in d:
            print ("".join(map(str, elem)))
        return
    d.append(m)
    d = d[-5:]
    for elem in d:
        print ("".join(map(str, elem)))


def show_stocks(d):
    #for k, v in d.items():
        #print(k,"\t\t",v)

    # Get the longest subject name
    length = max(len(x) for x in d)
    # decide on padding
    padding = 5

    #use these two value to working out the exact space required
    space = length + padding

    #format and print the statement
    for key, value in d.items():
        stock = "{0:{space}}".format(key, space=space)
        price = "{:.2f}".format(value)
        print(stock + price)

def show_owned(d):
    # Get the longest subject name
    length = max(len(x) for x in d)
    # decide on padding
    padding = 5

    #use these two value to working out the exact space required
    space = length + padding

    #format and print the statement
    for key, value in d.items():
        stock = "{0:{space}}".format(key, space=space)
        price = str(value)
        print(stock + price)

def stock_update_screen(stocks, owned, cash):
    print("\nStock Market\t Cash: $", cash,"\n------------------------------")
    # Get the longest subject name
    length = max(len(x) for x in stocks)
    # decide on padding
    padding = 5

    #use these two value to working out the exact space required
    space = length + padding

    #format and print the statement
    for key, value in stocks.items():
        stock = "{0:{space}}".format(key, space=space)
        price = "{:.2f}".format(value, space = space)
        ownership = str(owneddict[key])
        print(stock + price + "\t" + ownership)

def stock_graph(stocks, owned, cash):

    # Get the longest subject name
    length = max(len(x) for x in stocks)
    # decide on padding
    padding = 5

    #use these two value to working out the exact space required
    space = length + padding

    os.system('cls' if os.name == 'nt' else 'clear') #Wipe terminal clean
    #print("\nStock Market\t Cash: $", int(cash),"\n--------------------------------" + ("-" * int(stocks[max(stocks, key = stocks.get)]/0.05)))
    print("\nStock Market\t Cash: $", int(cash),"\n" + ("-" * 72))

    #format and print the statement
    for key, value in stocks.items():
        stock = "{0:{space}}".format(key, space=space)
        price = "{:.2f}".format(value, space = space)
        pricegraph = "|" * int(value/0.05)
        #Show midline at 1.00
        if value >= 1.00:
            pricegraph = replace_str_index(pricegraph, 19, "X")
        ownership = str(owned[key])
        print(stock + price + "\t" + ownership + "\t" + pricegraph)


def advancement(stock_data, owned, rolls, cash, d, speedmode = False):
    for _ in range(rolls):

        r1 = randint(0, 2)  # 0: div, 1: up, 2: down
        #r2 = randint(0, 5)  # 0: stock1, 1: stock2, ... , 5: stock6
        r2 = choice(list(stock_data.keys()))
        r3 = randint(0, 2)  # 0: 5, 1: 10, 2: 20

        if r3 == 0:
            num = 0.05
        elif r3 == 1:
            num = 0.10
        else:
            num = 0.20

        #Convert die roll to
        if r1 == 0 and stock_data[r2] >= 1:
            #Check ownership first
            stock_graph(stock_data, owned, cash)
            messages(d)
            if owned[r2] > 0:
                cash += (owned[r2] * num)
                #Stock graph is here instead of the end of the loop so that the
                #Console clearing doesn't remove the notifications.
                stock_graph(stock_data, owned, cash)
                text = "Dividends paid from ", r2, " for $", int(owned[r2]*num)
                messages(d, text)
        elif r1 == 1:
            stock_data[r2] += num
            stock_graph(stock_data, owned, cash)
            messages(d)
            if stock_data[r2] >= 2:
                stock_data[r2] = 1
                owned[r2] *= 2
                stock_graph(stock_data, owned, cash)
                text = r2, " split! Shares doubled."
                messages(d, text)
        elif r1 == 2:
            stock_data[r2] -= num
            stock_graph(stock_data, owned, cash)
            messages(d)
            if stock_data[r2] <= 0:
                stock_data[r2] = 1
                owned[r2] = 0
                stock_graph(stock_data, owned, cash)
                text = r2, " crashed! All shares lost."
                messages(d, text)
        if speedmode == False:
            time.sleep(0.25)
    #stock_graph(stock_data, owned, cash)
    return stock_data, owned, cash

#def main(cash, stockdict, owneddict, shortdict, players, rounds, rolls, turns_per_round):
def main():

    #Message buffer
    d = []

    #Speed mode?
    speedmode = False

    #Moved constants and initial setup to here when everything moved into main()
    cash = 5000
    players = 8
    turns_per_round = 7
    rounds = 90
    rolls = players*turns_per_round

    stockdict = {
        "Oil" : 1.00,
        "Gold" : 1.00,
        "Silver" : 1.00,
        "Bonds" : 1.00,
        "Grain" : 1.00,
        "Industrial" : 1.00
    }

    owneddict = {
        "Oil" : 0,
        "Gold" : 0,
        "Silver" : 0,
        "Bonds" : 0,
        "Grain" : 0,
        "Industrial" : 0
    }

    shortdict = {
            "Oi" : "Oil",
            "Go" : "Gold",
            "Si" : "Silver",
            "Bo" : "Bonds",
            "Gr" : "Grain",
            "In" : "Industrial",
            }

    #Begin a round
    #Offer to buy
    break_check = False #Used to offer a way to quit the game without issue.

    #--------------------------------------------------------------------------#
    #Auto-Pilot Setup#
    autopilot = False
    autolower = 1.15
    autoupper = 1.40

    for roundcount in range(rounds):
        #Ask for speedmode on round 1:
        if roundcount == 0:
            os.system('cls' if os.name == 'nt' else 'clear') #Wipe terminal clean
            ask = input("Would you like to accelerate the markets to maximum speed?\nThis will make it impossible to follow to markets in real time,\n but makes the game much quicker. (y/n):").lower()
            if ask == "y":
                speedmode = True
        purchaseround = True

        #Quick check for if player is completely broke
        if sum(owneddict.values()) == 0 and cash <= 2:
            purchaseround = False
            break_check = True
            print("You're broke! Game Over.")
            break

        #Check for auto-pilot
        if autopilot == True:
            purchaseround = False
            purchaselist = []
            #Auto sell anything above or below 1.15 - 1.40
            for key, value in stockdict.items():
                #Check if out of range
                if value < autolower or value > autoupper:
                    #Sell entire holdings at current value
                    cash += value*owneddict[key]
                    owneddict[key] = 0
                    text = "Auto: Sold all ", key
                    stock_graph(stockdict, owneddict, cash)
                    messages(d, text)
                else:
                    #Purchase max possible if within range. Note that because of
                    #the order of operations, some cash might not be spent after
                    purchaselist.append(key)

            #Division of cash for purchases:
            if len(purchaselist) > 0:
                purchasecash = floor(cash/len(purchaselist))
                for i in range(len(purchaselist)):
                    owneddict[purchaselist[i]] += myround(floor(purchasecash/stockdict[purchaselist[i]])) #Greatest int <= x
                    #myround adds a restriction that 500 is the smallest divisible unit to buy of a stock, just like players
                    cash -= floor(purchasecash/value)*value
                    text = "Auto: Bought max ", purchaselist[i]
                    stock_graph(stockdict, owneddict, cash)
                    messages(d, text)

                messages(d, "Autopilot marketing complete.")
            if speedmode == False:
                time.sleep(1)


        while purchaseround == True:
            bors = input ("Buy, sell, continue, or exit? (b/s/c/e): ").lower()
            if bors == "e":
                break_check = True
                break
            if bors == "c":
                purchaseround = False
            #---------------------------------------------------------------------#
            if bors == "autopilot":
                autopilot = True
                owneddict["Oil"] += 1000
                owneddict["Gold"] += 1000
                owneddict["Silver"] += 1000
                owneddict["Bonds"] += 1000
                owneddict["Grain"] += 500
                owneddict["Industrial"] += 500
                cash -= 5000
                purchaseround = False
            #---------------------------------------------------------------------#
            if bors == "b":
                stock_graph(stockdict, owneddict, cash)
                stock2purch = input("Which stock would you like to buy? (First 2 letters acceptable): ").title()
                if len(stock2purch) == 2:
                    stock2purch = shortdict[stock2purch]
                if stock2purch in stockdict:
                    amounts = input("How many would you like to buy? (#/$#/max): ")
                    if amounts == "max":
                        amounts = myround(floor(cash/stockdict[stock2purch])) #Greatest int <= x
                        #myround adds a restriction that 500 is the smallest divisible unit to buy of a stock, just like players
                    elif "$" in amounts:
                        #amounts = [int(s) for s in amounts.split() if s.isdigit()] #Extract the number from the input
                        #amounts = int(list(filter(str.isdigit, amounts))[0])
                        amounts = int(re.search('\d+', amounts).group())
                        amounts = int(amounts/stockdict[stock2purch])
                    else:
                        amounts = int(amounts)

                    #Check funds
                    if amounts*stockdict[stock2purch] > cash:
                        print("Not enough funds,", int(amounts*stockdict[stock2purch]), "needed.\n", int(cash), "available.")
                    else:
                        #Subtract cash and add stock value.
                        cash -= amounts*stockdict[stock2purch]
                        owneddict[stock2purch] += amounts
                        stock_graph(stockdict, owneddict, cash)
                        print("Purchased", amounts, stock2purch, "for $", int(amounts*stockdict[stock2purch]))
                else:
                    print("Invalid stock option")

            #---------------------------------------------------------------------#
            if bors == "s":
                stock_graph(stockdict, owneddict, cash)
                stock2purch = input("Which stock would you like to sell? (First 2 letters acceptable): ").title()
                if len(stock2purch) == 2:
                    stock2purch = shortdict[stock2purch]
                if stock2purch in stockdict:
                    amounts = int(input("How many would you like to sell?: "))

                    #Check if you hold that much
                    if amounts > owneddict[stock2purch]:
                        print("Not enough stock to sell,", amounts, "needed.\n", owneddict[stock2purch], "available.")
                    else:
                        #Add cash and subtract stock value.
                        cash += amounts*stockdict[stock2purch]
                        owneddict[stock2purch] -= amounts
                        stock_graph(stockdict, owneddict, cash)
                        print("Sold", amounts, stock2purch, "for $", int(amounts*stockdict[stock2purch]))
                else:
                    print("Invalid stock option")

            #Quick shortcut for purchases to test program with
            if bors == "t":
                owneddict["Oil"] += 1000
                owneddict["Gold"] += 1000
                owneddict["Silver"] += 1000
                owneddict["Bonds"] += 1000
                owneddict["Grain"] += 500
                owneddict["Industrial"] += 500
                cash -= 5000
                stock_graph(stockdict, owneddict, cash)


        #Launch stock update cycle.
        if break_check == True:
            break
        stockdict, owneddict, cash = advancement(stockdict, owneddict, rolls, cash, d, speedmode = speedmode)
        #time.sleep(0.5)


    stock_graph(stockdict, owneddict, cash)
    print("\nGAME COMPLETED")

    invested = 0
    for key, value in stockdict.items():
        invested += owneddict[key] * value
        #print(owneddict[key] * value)
    print("Final score: $", int(invested + cash - 5000))

if __name__ == "__main__":
    main()

'''
x, y_E, y_SD = [], [], []
plot_left = 5  # 40
plot_right = 195  # 60
#  use the commented views to for a better lens into what's actually happening - remove extremes
n_lst = []

for k in range(1, 40):
    if 5*k in dat:
        n = len(dat[5 * k][0])
        n_lst.append(n)
        if n > 0:
            div_stats = [np.mean(dat[5 * k][0]), np.std(dat[5 * k][0])]
            hold_stats = [np.mean(dat[5 * k][1]), np.std(dat[5 * k][1])]
            profit_stats = [np.mean(dat[5 * k][2]), np.std(dat[5 * k][2])]

            s1 = "${:.2f}".format(div_stats[0])
            s2 = "${:.2f}".format(hold_stats[0])
            s3 = "${:.2f}".format(profit_stats[0])
            s4 = "${:.2f}".format(profit_stats[1])
            print("S = {:<10} n = {:<10} E[D] = {:<10} E[H] = {:<10} E[P] = {:10} SD[P] = {:10}".
                  format(5*k, n, s1, s2, s3, s4))
            if plot_left <= 5*k <= plot_right:
                x.append(5 * k)
                y_E.append(profit_stats[0])
                y_SD.append(profit_stats[1])

    else:
        n_lst.append(0)

out = open(name_id + "dat.pickle", "wb")
pickle.dump(dat, out)
out.close()

fig, ax = plt.subplots()

ax.axvline(100, color='k', ls="dashed", label="Par", zorder=-10)
ax.scatter(x, y_E, color='c', label="Expected Value")
ax.scatter(x, y_SD, color='r', label="Standard Deviation")


ax.legend(loc="upper right")

formatter = tck.FormatStrFormatter("$%.0f")
ax.yaxis.set_major_formatter(formatter)

for tick in ax.yaxis.get_major_ticks():
    tick.label1.set_color('green')

plt.xlabel("Initial Stock Value")
plt.title("~{} Profit Simulations Per Stock Value".format(int(np.mean(n_lst))))

plt.show()
'''
