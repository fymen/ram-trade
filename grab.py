#!/usr/bin/python3
import json
import sys
import os
import math
import time

import config
from ram_op import *

fee_rate = 0.005


OP_INIT = 0
OP_FIND_BUY_POINT = 1
OP_FIND_SELL_POINT = 2

# profit would gain
def get_profit(quantity,price_buy, price_sell):
    return (pow((1 - fee_rate), 2) * price_sell / price_buy - 1) * quantity

def get_profit_ratio(price_buy, price_sell):
    return (pow((1 - fee_rate), 2) * price_sell / price_buy - 1)

# anticipate profit price
def get_profit_price(buy_price):
    return buy_price / pow((1 - fee_rate), 2)

def main():
    simulate = 1
    i = 0
    
    ram = ram_op()
    
    f = open('./test.txt', 'wt')
    
    
    print("date\t\t\tcur\t\tmax\t\tmin")

    op_status = OP_INIT

    max_price = min_price = ram.get_ram_price(simulate)
    
    while 1:
        current_price = ram.get_ram_price(simulate);
        if (current_price == -1):
            continue
    
        if (current_price > max_price):
            max_price = current_price
        elif (current_price < min_price):
            min_price = current_price

        if(op_status == OP_INIT):
            eos2buyram = 4.0

            ram_old = ram_bought = 0
            buy_price = 0
            ratio = 0

            op_status = OP_FIND_BUY_POINT
            
        elif (op_status == OP_FIND_BUY_POINT):
            if (((min_price / max_price) < 0.94) and ((current_price - min_price) < 0.0001)):
                ram_old = ram.get_account_ram(simulate)
                ram.buy_ram(simulate, eos2buyram)

                if (simulate == 1):
                    ram.virtual_ram_update(eos2buyram, current_price)
                
                time.sleep(0.5)
                ram_bought = ram.get_account_ram(simulate) - ram_old
                if (ram_bought <= 0):
                    print("bought ram error %d" % (ram_bought));
                    break;
                buy_price = eos2buyram / ram_bought
                
                op_status = OP_FIND_SELL_POINT
                
        elif(op_status == OP_FIND_SELL_POINT):
            ratio = get_profit_ratio(buy_price, current_price)
            if (ratio > 0.03):
                ram.sell_ram(simulate, ram_bought)
                print("profit: %f EOS" % (eos2buyram * ratio) )
                
                op_status = OP_INIT
        else:
            print("should not be here, %d" % op_status)
            
        # print(get_profit(init_quantity, buy_price, current_price))

        cur_time = time.strftime("%H:%M:%S")

        # print("%s\t%f\t%f\t%f\top_status:%d ratio:%f bought price: %f" % (cur_time, current_price, max_price, min_price, op_status, ratio, buy_price))

        # f.write("%s\t%f\t%f\t%f" % (cur_time, current_price, max_price, min_price))
        # f.flush()

        # i = i + 1
        if (simulate == 1) :
            gap = 0.001
        else:
            gap = 1
            
        time.sleep(gap)

    f.close()
    # data.close()
    
if __name__ == "__main__":
    main()

