'''
app_folder/urlsからの決定を決定をうけて、処理を処理を決定する
'''

#import csv
#import io
import os
#import requests
#import json
import shutil
#from django import forms
from django.shortcuts import render
from django.shortcuts import redirect
#from django.conf import settings
#from django.views import View,generic
#from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
#from ..models import BookListModel
#from ..models import DisposalListModel
#from .models import Upload
from ..forms import BookRegistForm
#from ..forms import DisposalListForm
#from ..forms import UploadForm
from .search_book import search_book
from .img_to_isbn import img_to_isbn
from PIL import Image,ImageFilter
#from datetime import datetime,date


from . import app_settings
app_settings.init()

#バーコードスキャン
def input_barcode(request):
    context=app_settings.context
    if context['ms_flag'] == 0:
        context['message'] = ""

    #GETのとき（初回表示）初期化

    #POSTで画像がないとき
    if request.method == 'POST' and request.FILES == None:
        context["message"] ="myfileがNULLです。バーコードを撮影、またはバーコード画像を選択してください "
        #return render(request,'app_folder/input_barcode.html',context)
        return redirect ('app_folder/input_barcode.html')

    #POSTで画像があるとき
    elif request.method == 'POST' and request.FILES['myfile']:
        #画像ファイル名取得
        if request.FILES['myfile']:
            myfile = request.FILES['myfile']
        else:
            context["message"] += "画像が読み込めませんでした。画像を再撮影してください"
            return render(request,'app_folder/input_barcode.html',context)

        #画像ファイル取得
        fs = FileSystemStorage()

        #画像ファイル保存とファイル名取得
        filename = fs.save(myfile.name,myfile)

        #ファイルのアドレス取得
        uploaded_file_url = fs.url(filename)
        if uploaded_file_url == None:
            #context["uploaded_file_url"] = uploaded_file_url
            context["message"] = "画像が読み込めませんでした "
            return redirect ('app_folder/input_barcode.html')
            #return render(request,'app_folder/input_barcode.html',context)

        #画像からISBN取得
        image_url = '/home/ao26jan/mysite' + uploaded_file_url
        img = Image.open(image_url)
        isbn = img_to_isbn(img)
        if isbn==None:
            context["message"] = "ISBNが認識できませんでした。再度撮影し直してください"
            os.remove(image_url)
            return render(request,'app_folder/input_barcode.html',context)

        #ISBNから書誌情報取得
        bookdata_dict = search_book(isbn)

        #context["bookdata_dict"] = bookdata_dict
        if bookdata_dict['result'] == 'error':
            context['message'] = "ISBN:" + isbn + " で検索しましたが見つかりませんでした。"
            os.remove(image_url)
            return render(request, 'app_folder/input_barcode.html',context)

        #formにbookdata_dictを差し込み
        form = BookRegistForm(bookdata_dict)
        title = bookdata_dict['title']

        #書籍情報を保存
        if form.is_valid():
            form.save(commit=True) #データ登録
            context['message'] = '■「' + title + '」が登録されました！\n'
            context['ms_flag'] = 1
            context['bookdata_dict'] = bookdata_dict
            context['form'] = form
            os.remove(image_url)
            shutil.rmtree('/home/ao26jan/mysite/media/')
            os.mkdir('/home/ao26jan/mysite/media/')
            return redirect('../')
            #render(request,'app_folder/input_barcode.html',context)
        else:
            #for ele in form:
            #    message = message + "\n" + ele
            context['message'] = '・バリテーションエラーのため登録できませんでした\n'
            context['bookdata_dict'] = bookdata_dict
            context['form'] = form
            #return redirect('../')
            return render(request,'app_folder/input_barcode.html',context)

        os.remove(image_url)

    return render(request, 'app_folder/input_barcode.html',context)