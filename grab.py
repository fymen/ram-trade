#!/usr/bin/python3
import json
import sys
import os
import math
import time
import signal
import argparse

import config
from ram_op import *
from plot import *


fee_rate = 0.005
time_format = "%m-%d,%H:%M:%S"

log_ram_price = "ram_price.txt"
log_bought_points = "bought_points.txt"
log_sold_points = "sold_points.txt"

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

is_sigint_up = False

def sigint_handler(signum, frame):
    global is_sigint_up
    is_sigint_up = True
    print ('catched interrupt signal!')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="debug verbose mode",
                        action="store_true")
    parser.add_argument("-v", "--verbose", help="info verbose mode",
                        action="store_true")
    parser.add_argument("-p", "--plot", help="plot out instantly by gnuplot", action="store_true")
    parser.add_argument("-s", "--simulate", type=str, 
                        help="simulate ")
    args = parser.parse_args()
    
    ram = ram_op()

    simulate = False
    if (args.simulate) :
        simulate = ram.open_simulate_file(args.simulate) == True
        
    if (args.plot) :
        plot = gnuplot()
    
    f = open(log_ram_price, 'wt')
    f_points = open(log_bought_points, 'wt')
    f_sell_points = open(log_sold_points, 'wt')

    boughts = solds = 0
    i = 0
    
    print("date\t\t\tcur\t\tmax\t\tmin")

    op_status = OP_INIT

    max_price = min_price = ram.get_ram_price()
    
    while 1:
        signal.signal(signal.SIGINT, sigint_handler)
        if (is_sigint_up == True):
            break
        #以下那句在windows python2.4不通过,但在freebsd下通过
        signal.signal(signal.SIGHUP, sigint_handler)
         
        signal.signal(signal.SIGTERM, sigint_handler)

        
        current_price = ram.get_ram_price();
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

            buy_count = 0
            
            op_status = OP_FIND_BUY_POINT
            
        elif (op_status == OP_FIND_BUY_POINT):
            if (((min_price / max_price) < 0.94) and ((current_price/max_price) < 0.94)):
                buy_count += 1
                if (buy_count > 10) :
                    ram_old = ram.get_account_ram()
                    ram.buy_ram(eos2buyram)

                    if (simulate):
                        ram.virtual_ram_update(eos2buyram, current_price)
                
                    time.sleep(0.5)
                    ram_bought = ram.get_account_ram() - ram_old
                    if (ram_bought <= 0):
                        print("bought ram error %d" % (ram_bought));
                        break;
                    buy_price = eos2buyram / ram_bought
                    
                    f_points.write("%s\t%d\t%f\n" % (time.strftime(time_format), i, buy_price))
                    f_points.flush()
                    boughts += 1

                    op_status = OP_FIND_SELL_POINT
                
        elif(op_status == OP_FIND_SELL_POINT):
            ratio = get_profit_ratio(buy_price, current_price)
            if (ratio > 0.03):
                ram.sell_ram(ram_bought)
                profit = eos2buyram * ratio
                print("profit: %f EOS" % (profit) )

                f_sell_points.write("%s\t%d\t%f\t%f\n" % (time.strftime(time_format), i, current_price, profit))
                f_sell_points.flush()
                solds += 1
                
                op_status = OP_INIT
        else:
            print("should not be here, %d" % op_status)
            
        # print(get_profit(init_quantity, buy_price, current_price))

        cur_time = time.strftime(time_format)
        if (args.verbose):
            print("%s\t%f\t%f\t%f\top_status:%d ratio:%f bought price: %f" % (cur_time, current_price, max_price, min_price, op_status, ratio, buy_price))

        f.write("%s\t%f\n" % (cur_time, current_price))
        f.flush()

        
        if ((i % 4 == 0) and (args.plot)):
            plot_ram = "'" + log_ram_price + "'" + " using 0:2 with line, "
            if (boughts > 0):
                plot_buy_point = "'" + log_bought_points + "'" + " using 2:3 pointtype 148 ps 2 lc rgb \"blue\" title \"buy point\", "
            else:
                plot_buy_point = " "

            if (solds > 0):
                plot_sell_point = "'" + log_sold_points + "'" + " using 2:3 pointtype 7 ps 2 lc rgb \"red\" title \"sell point\", "
            else:
                plot_sell_point = " "
                
            plot_min = str(min_price) + " with line, "
            plot_max = str(max_price) + " with line "

            plot.plot(plot_ram + plot_buy_point + plot_sell_point + plot_min + plot_max)
        
        if (simulate) :
            gap = 0.0008
        else:
            gap = 1

        i = i + 1
        time.sleep(gap)

    f.close()
    f_points.close()
    f_sell_points.close()
    if (simulate) :
        ram.close_simulate_file()
    
    # data.close()
    
if __name__ == "__main__":
    main()

