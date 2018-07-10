#!/usr/bin/python3
import json
import sys
import os
import math
import time

import config


# http://api-mainnet.starteos.io
# http://mainnet.eoscanada.com
# http://mainnet.eoscalgary.io
# http://mainnet.eoscannon.io
# http://mainnet.genereos.io
# cleos = "cleos --wallet-url http://127.0.0.1:8900 -u http://mainnet.genereos.io "
cleos = "cleos --wallet-url http://127.0.0.1:8900 -u http://mainnet.eoscanada.com "

default_password = "PW5JdsEXgifmmdJnJvdyMpfwR6bcg6EKVb8hpcTmygNANhGrrVEU2"
op_account = "blondebeauty"



class ram_op():
    def __init__(self):
        self.test_init_ram = 4
        self.simulate = False
        
    def open_simulate_file(self, simulate_data_file):
        try:
            self.data = open(simulate_data_file, 'r')
        except IOError:
            print("open %s error" % simulate_data_file)
        else:
            self.simulate = True

        return self.simulate

    def close_simulate_file(self):
        self.data.close()
        self.simulate = False
        
    def get_ram_price(self):
        if (self.simulate):
            price = float(self.data.readline())
            return price
            
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


    def unlock_wallet(self):
        cmd = cleos + "wallet unlock --password" + " " + default_password
        os.system(cmd)
        
    def buy_ram(self, eos_no):
            
        if (eos_no <= 0):
            print("buy ram error: %f" % eos_no)

        if (self.simulate == True):
            print("simulate buy ram %d" % eos_no)
        else:
            self.unlock_wallet()
    
            print("buy ram")
            cmd = cleos + "system buyram  " + op_account + " " + op_account + " " + "'" + str(eos_no) + " EOS'"
            print(cmd)
            os.system(cmd)

    
    def sell_ram(self, ram_no):
        if (ram_no <= 0):
            print("sell ram error: %f" % ram_no)

        if (self.simulate == True):
            print("simulate sell ram %d" % ram_no)
        else:
            if (ram_no <= 0):
                print("sell ram error: %f" % ram_no)
                print("buy ram")
                
            self.unlock_wallet()
    
            cmd = cleos + "system sellram " + op_account + " " + str(int(ram_no*1024))
            print(cmd)
            os.system(cmd)

    def get_account_ram(self):
        if (self.simulate):
            return self.test_init_ram
            
        cmd = cleos + "get account " + op_account + " -j"
        process = os.popen(cmd)
        output = process.read()
        if (len(output) == 0) :
            print("get ram table error")
            return -1
        account_info = json.loads(output)
        # print(output)
        return float(account_info["total_resources"]["ram_bytes"]) / 1024


    def virtual_ram_update(self, eos, price):
        self.test_init_ram = self.test_init_ram + eos / price


    
def main():
    ram = ram_op()
    ram.open_simulate_file('1m.txt')

    # ram.buy_ram(0.001)
    # ram.sell_ram(0.001)
    while 1:
        print(ram.get_ram_price())

        time.sleep(1)

if __name__ == "__main__":
    main()
