#!/usr/bin/env python

#--------NASDAQ Listener----------
'''
Writen By: Oliver Hoare
Date: 31/12/19
Description: CSV NASDAQ data grabber. Produces the financial index data in CSV form.
'''


import urllib2
import csv
import time

def import_web(ticker):
    url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol='+ticker+'&apikey=ME91QW9B9OC9PBJ8&datatype=csv'
    fp = urllib2.urlopen(url)
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()
    return mystr

def get_value(ticker):
    print(ticker)
    js = import_web(ticker)
    save_data(js,ticker)


def save_data(js,ticker):
    mystring = js.split('\r\n')
    a = len(mystring)
    for i in range(a):
        substring = mystring[i]
        substring = substring.split(',')
        mystring[i] = substring

    #make directory
    path = 'MSFT_NASDAQ.csv'
    writer = csv.writer(open(path, 'ab'), delimiter = ',')

    tim = time.strftime('%H%M')
    timestamp = mystring[1][6] + ' ' + tim[2:] + ':' + tim[:2]
    writer.writerow([timestamp, mystring[1][1], mystring[1][4], mystring[1][9]])

def main():
    # Start Process
    company_list = ['MSFT']
    try:
        for company in company_list:
            print("Starting with " + company)
            get_value(company)
            print("Ended Writing Data of " + company)
    except Exception as e:
        print(e)

main()
