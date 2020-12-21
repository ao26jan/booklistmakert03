'''
ISBNから書籍情報を取得する関数
'''
import requests
import json
import time
import re
import sys
import math
from django.http import HttpResponse

def search_book(isbn):
    search_result ={}
    #isbn = '978' + isbn
    #print('searching ...ISBN:',isbn)
    #print("インデックス：" + str(index) + ", 値：" + val)
    #いくつかの引数を加えたURL
    url = 'https://app.rakuten.co.jp/services/api/BooksTotal/Search/20170404?format=json&keyword=%E6%9C%AC&booksGenreId=000&isbnjan=' + isbn + '&applicationId=1049247665618959244'
    #return HttpResponse("URL :  %s" % url)
    #print('url:',url,'\n')
    #responsetime
    rq = requests.get(url)
    #print('rq is : ',rq,'\n')
    #jsonとしてloadするための前処理
    #strip関数を使いcallback(と);を取り除く,I
    #prejsn = rq.text.strip('callback(').strip(');')
    prejsn = rq.text.strip('[').strip(']') #str型

    try:
        jsn = json.loads(prejsn)
        #pprint.pprint(jsn)
        #onix部のみを抽出する
        session = jsn
        #pprint.pprint(jsn)
    except json.decoder.JSONDecodeError:
        #print('Server Error')
        #session部がない場合はサーバーエラーとして処理
        #その場合はプログラム終了
        sys.exit()

    if jsn['hits'] != 0:
        #jsnがNoneではない場合
        result = "success"
        title = jsn['Items'][0]['Item']['title']
        author = jsn['Items'][0]['Item']['author']
        detail = jsn['Items'][0]['Item']['itemCaption']
        publisher = jsn['Items'][0]['Item']['publisherName']
        date = jsn['Items'][0]['Item']['salesDate']
        date = date[0:4]
        price = str(jsn['Items'][0]['Item']['itemPrice'])
        price = math.ceil(int(price)/1.1)
    else:
        result = "error"
        title = ""
        author = ""
        detail = ""
        publisher = ""
        date = ""
        price = ""

    #辞書型に結果格納
    search_result.update({'result':result,'publisher':publisher,'title':title,'author':author,'price':price,'detail':detail,'date':date,'isbn':isbn})

    return search_result