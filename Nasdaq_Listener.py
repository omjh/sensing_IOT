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
    """
    :param identifier: List, Takes the company name
    :return:displays companies records per minute
    """
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&amp;symbol=' + ticker + '&amp;interval=5min&amp;apikey='+ 'ME91QW9B9OC9PBJ8'+ '&amp;outputsize=full&amp;datatype=csv'
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
    a = len(mystring)-2
    print (a)
    for i in range(a):
        substring = mystring[i]
        substring = substring.split(',')
        mystring[i] = substring

    #make directory
    date_latest = mystring[1][0][:10]
    print(date_latest)
    path = 'MSFT_NASDAQ.csv'

    writer = csv.writer(open(path, 'wb'), delimiter = ',')

    writer.writerow([mystring[0][0],mystring[0][1],mystring[0][4], 'changePercent'])
    print(mystring[0])
    for i in range(a-2):
        if mystring[a-2-i][1] != '-' and mystring[a-2-i][4] != '-':
            print(mystring[a-2-i][1]),float(mystring[a-2-i][4])
            percent_change = (float(mystring[a-2-i][1])-float(mystring[a-2-i][4]))/float(mystring[a-2-i][1])*100
            writer.writerow([mystring[a-2-i][0],mystring[a-2-i][1],mystring[a-2-i][4],percent_change])
            print(i)

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
