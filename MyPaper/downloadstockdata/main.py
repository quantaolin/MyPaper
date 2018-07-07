from pymongo import MongoClient
import tushare as ts
import time
'''
Created on 2018-07-07 09:17

@author: quantaolin
'''

conn = MongoClient('127.0.0.1', 27017)
db = conn.mydb

sb_set = db.sb_set
sb = ts.get_stock_basics()

#get stock code list
# for indx,item in sb.iterrows():
#     date = sb.ix[indx]['timeToMarket']
#     sb_set.insert({"code":indx,"industry":item['industry'],"area":item['area'],"pe":item['pe'],"outstanding":item['outstanding'],"timeToMarket":int(date)})

#get stock data
for i in sb_set.find():
    code = i['code']
    #1.check data is exist
    collist = db.collection_names()
    if code in collist:
        print("code:",code," is already getted continue")
        continue
    #2.get start date
    timeToMarket = i['timeToMarket']
    start_date = "2013-01-01"
    print("get data for code:",code,".timeToMarket:" + str(timeToMarket))
    if timeToMarket>20130101:
        t = str(timeToMarket)
        start_date = t[0:4] + "-" + t[4:6] + "-" + t[6:]
    #3.get data , if fail try again
    tmp_set = db[code]
    df=None
    wait_time = 300
    while True:
        try:
            df = ts.get_h_data(code,start= start_date,end= '2018-07-06')
        except IOError:
            print("get fail ,wait....",wait_time,"sec")
            time.sleep(wait_time)
            continue
        else:
            break
    #4.insert mongodb
    for indx,item in df.iterrows():
        tmp_set.insert({"data":indx,"close":item['close'],"volume":item['volume'],"high":item['high'],"close":item['close']})  