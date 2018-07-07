#!/usr/bin/python3
import json
import sys
import os
import math
import time

from numpy import *
import Gnuplot, Gnuplot.funcutils


cleos = "cleos --wallet-url http://127.0.0.1:8900 -u http://mainnet.genereos.io "

default_password = "PW5JdsEXgifmmdJnJvdyMpfwR6bcg6EKVb8hpcTmygNANhGrrVEU2"

op_account = "blondebeauty"
fee_rate = 0.005

# simulate
# test_init_ram = 4
# data = open('./1m.txt', 'r')




def get_ram_price():
    cmd = cleos + "get table eosio eosio rammarket"

    # print("cmd: %s" % cmd);
    
    process = os.popen(cmd)
    output = process.read()
    if (len(output) == 0) :
        print("get ram table error")
        return -1

    # print(output)
    
    ram_table = json.loads(output)
    rows = ram_table["rows"]
    base_balance = rows[0]["base"]["balance"].split(' ')

    # 
    # formula: price=0.0149012/((1-U)^2)
    # 
    ram_balance = float(base_balance[0])
    balance_percent = ram_balance / 1024 / 1024 / (64*1024)
    # print(balance_percent)
    price = 0.0149012 / pow(balance_percent, 2)

    # print(ram_balance)
    # print(price)
    return price

# simulate
    # price = float(data.readline())
    # return price

def unlock_wallet():
    cmd = cleos + "wallet unlock --password" + " " + default_password
    os.system(cmd)

# profit would gain
def get_profit(quantity,price_buy, price_sell):
    return (pow((1 - fee_rate), 2) * price_sell / price_buy - 1) * quantity

def get_profit_ratio(price_buy, price_sell):
    return (pow((1 - fee_rate), 2) * price_sell / price_buy - 1)

# anticipate profit price
def get_profit_price(buy_price):
    return buy_price / pow((1 - fee_rate), 2)

def buy_ram(eos_no):
    if (eos_no <= 0):
        print("buy ram error: %f" % eos_no)

    unlock_wallet()
    
    print("buy ram")
    cmd = cleos + "system buyram  " + op_account + " " + op_account + " " + "'" + str(eos_no) + " EOS'"
    print(cmd)
    os.system(cmd)

    
def sell_ram(ram_no):
    if (ram_no <= 0):
        print("sell ram error: %f" % ram_no)
    print("buy ram")

    unlock_wallet()
    
    cmd = cleos + "system sellram " + op_account + " " + str(int(ram_no*1024))
    print(cmd)
    os.system(cmd)

def get_account_ram():
    cmd = cleos + "get account " + op_account + " -j"
    process = os.popen(cmd)
    output = process.read()
    if (len(output) == 0) :
        print("get ram table error")
        return -1
    account_info = json.loads(output)
    # print(output)
    return float(account_info["total_resources"]["ram_bytes"]) / 1024

# simulate
    # return test_init_ram

def virtual_ram_update(eos, price):
    global test_init_ram
    test_init_ram = test_init_ram + eos / price

def main():
    # print(get_profit(10, 0.338, 0.365))
    # print(get_profit_price(0.43))
    f = open('./test.txt', 'wt')

    

    max_price = min_price = get_ram_price()

    init_quantity = 5
    sell_price = buy_price = 0.51
    ram_bought = 0
    
    RAM_WAIT4SELL = 0
    
    f = open('./test.txt', 'wt')

    # g = Gnuplot.Gnuplot(debug=1)
    # g.title('A simple example') # (optional)
    # g('set style data linespoints') # give gnuplot an arbitrary command
    # g('set xdata time')
    # g('set timefmt "%H:%M:%S" ')
    # g('set autoscale y')
    # g('set xrange ["16:25":"17:00"]')
    # g('set grid')
    
    # f.write("test.......%f............" % buy_price)
    # f.flush()
    i = 0
    
    print("date\t\t\tcur\t\tmax\t\tmin")

    print(get_account_ram())

    while 1:
        current_price = get_ram_price();
        if (current_price == -1):
            continue
    
        if (current_price > max_price):
            max_price = current_price
        elif (current_price < min_price):
            min_price = current_price
            
        if (RAM_WAIT4SELL == 0):
            if (((min_price / max_price) < 0.94) and ((current_price - min_price) < 0.0001)):
                eos2buyram = 5.0
                ram_old = get_account_ram()
                buy_ram(eos2buyram)

                # simulate
                # virtual_ram_update(eos2buyram, current_price)
                
                time.sleep(0.5)
                ram_bought = get_account_ram() - ram_old
                if (ram_bought <= 0):
                    print("bought ram error %d" % (ram_bought));
                    break;
                buy_price = eos2buyram / ram_bought
                RAM_WAIT4SELL = 1
        elif(RAM_WAIT4SELL == 1):
            ratio = get_profit_ratio(buy_price, current_price)
            if (ratio > 0.05):
                sell_ram(ram_bought)
                print("profit: %f EOS" % (eos2buyram * ratio) )
                RAM_WAIT4SELL = 0
        else:
            nop
            
            
        # print(get_profit(init_quantity, buy_price, current_price))

        cur_time = time.strftime("%H:%M:%S")

        print("%s\t%f\t%f\t%f" % (cur_time, current_price, max_price, min_price))

        f.write("%s\t%f\t%f\t%f" % (cur_time, current_price, max_price, min_price))
        f.flush()

        # if (i % 4 == 0):
        #     g.plot("'test.txt' using 1:2")

        # i = i + 1
        time.sleep(0.5)


    f.close()
    # data.close()
if __name__ == "__main__":
    main()
    # buy_ram(0.01)
    # sell_ram(0.01)

