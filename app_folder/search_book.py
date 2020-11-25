import requests
import json
import time
import re
import sys
from django.http import HttpResponse

def search_book(isbn):
    search_result ={}
    isbn = '978' + isbn
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

    #jsnがNoneではない場合
    title = jsn['Items'][0]['Item']['title']
    author = jsn['Items'][0]['Item']['author']
    Detail = jsn['Items'][0]['Item']['itemCaption']
    Publisher = jsn['Items'][0]['Item']['publisherName']
    pubdate = jsn['Items'][0]['Item']['salesDate']
    price = jsn['Items'][0]['Item']['itemPrice']
    #辞書型に結果格納
    search_result.update({'出版社':Publisher,'書名':title,'著者':author,'単価':price,'詳細':Detail,'出版年月':pubdate,'ISBN':isbn})

    return search_result