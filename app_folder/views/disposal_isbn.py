'''
app_folder/urlsからの決定を決定をうけて、処理を処理を決定する
'''

#import csv
#import io
#import os
#import requests
#import json
#import shutil
#from django import forms
from django.shortcuts import render
#from django.shortcuts import redirect
#from django.conf import settings
#from django.views import View,generic
#from django.http import HttpResponse
#from django.core.files.storage import FileSystemStorage
#from .models import BookListModel
#from .models import DisposalListModel
#from .models import Upload
#from .forms import BookRegistForm
from ..forms import DisposalListForm
#from .forms import UploadForm
from .search_book import search_book
#from .img_to_isbn import img_to_isbn
#from PIL import Image,ImageFilter
from datetime import datetime,date


from . import app_settings
app_settings.init()

#ISBN入力
def disposal_isbn(request):
    context = app_settings.context
    if context['ms_flag'] == 0:
        context['message'] = ""
    #booklist = BookListModel.objects.all()
    if request.method == 'POST':
    # 画面からPOSTした場合
        isbn = '978' + request.POST['isbn']
        bookdata_dict = search_book(isbn)

        if bookdata_dict['result'] == 'error':
            context['message'] = 'ISBNから書籍がみつかりませんでした。'
            context['ms_flag'] = 1
            return render(request, 'app_folder/disposal_isbn.html',context)

        #bookdata_json = json.dumps(bookdata_dict) #JSONに変換
        #formにPOSTデータ書き込み。しないとバリテーションエラー

        bookdata_dict['disposal_date'] = date.today()
        #form = DisposalListForm(request.POST)
        #formにbookdata_dictを差し込み
        form = DisposalListForm(bookdata_dict)
        #return HttpResponse(form['publisher'])
        title = bookdata_dict['title']
        #today_v = datetime.date.today()
        #form = form( initial = {'disposal_date' :today_v} )
        #context['message']+=datetime.date.today()

        # 画面からPOSTした値を取得
        if form.is_valid():
            #form.save(commit=True) #データ登録
            context['message'] = '■ISBNから「' + title + '」が見つかりました。\n'
            context['ms_flag'] = 1
            context['bookdata_dict']=bookdata_dict
            context['form']=form
            return render(request,'app_folder/disposal_manual.html',context)
            #return redirect('../')
            #return render(request, '../app_folder/index.html',context)
        else:
            #for ele in form:
            #    message = message + "\n" + ele
            context['message'] = '■バリテーションエラーのため登録できませんでした'
            context['ms_flag'] = 1
            context['bookdata_dict'] = bookdata_dict
            context['form'] = form
            #return redirect('../')
            return render(request, 'app_folder/disposal_isbn.html',context)

    return render(request, 'app_folder/disposal_isbn.html',context)