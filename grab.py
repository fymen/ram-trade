#!/usr/bin/python3
import json
import sys
import os
import math
import time

def get_ram_price():
    cleos="cleos --wallet-url http://127.0.0.1:8900 -u http://mainnet.genereos.io "
    cmd=cleos + "get table eosio eosio rammarket"

    # print("cmd: %s" % cmd);
    
    process = os.popen(cmd)
    output = process.read()
    if (len(output) == 0) :
        print("get ram table error")
        sys.exit(0)

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
    
def main():
    while 1:
        print(get_ram_price())
        time.sleep(0.5)
            
if __name__ == "__main__":
    main()

