#!/usr/bin/python3
import urllib2
import json
import sys



def main():
    cmc_url="https://api.coinmarketcap.com/v1/ticker/"
    coin='bitcoin'
    fiat='CNY'

    url = cmc_url + coin + '?convet=' + fiat

    print(url)
    
    r = urllib2.urlopen(url, timeout = 5)
    test = json.load(r)
    print(test[0]['price_usd'])
    
main()

