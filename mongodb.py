from pymongo import MongoClient
import urllib.parse
import datetime

# Authentication Database認證資料庫
Authdb='stock-user_01'

##### 資料庫連接 #####
def constructor():
    client = MongoClient("mongodb://stock-user_01:isgoodgoodtime@cluster0-shard-00-00-is9rq.mongodb.net:27017,cluster0-shard-00-01-is9rq.mongodb.net:27017,cluster0-shard-00-02-is9rq.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client[Authdb]
    return db

#----------------------------儲存使用者的股票--------------------------
def write_user_stock_fountion(stock, bs, price):  
    db=constructor()
    collect = db['mystock']
    collect.insert({"stock": stock,
                    "data": 'care_stock',
                    "bs": bs,
                    "price": float(price),
                    "date_info": datetime.datetime.utcnow()
                    })
    
#----------------------------刪除使用者的股票--------------------------
def delete_user_stock_fountion(stock):  
    db=constructor()
    collect = db['mystock']
    collect.remove({"stock": stock})
    
#----------------------------顯示使用者的股票--------------------------
def show_user_stock_fountion():  
    db=constructor()
    collect = db['mystock']
    cel=list(collect.find({"data": 'care_stock'}))

    return cel
