'''
app_folder/urlsからの決定を決定をうけて、処理を処理を決定する
'''
import csv
#import io
#import os
#import requests
#import json
#import shutil
#from django import forms
#from django.shortcuts import render
#from django.shortcuts import redirect
#from django.conf import settings
#from django.views import View,generic
from django.http import HttpResponse
#from django.core.files.storage import FileSystemStorage
from ..models import BookListModel
from ..models import DisposalListModel
#from .models import Upload
#from ..forms import BookRegistForm
#from ..forms import DisposalListForm
#from ..forms import UploadForm
#from ..search_book import search_book
#from ..img_to_isbn import img_to_isbn
#from PIL import Image,ImageFilter

from . import app_settings
app_settings.init()

#ファイル出力
def csv_export(request):
    context=app_settings.context
    response = HttpResponse(content_type='text/csv')
    #ファイル名設定
    response['Content-Disposition'] = 'attachment; filename="booklist.csv"'
    # HttpResponseオブジェクトはファイルっぽいオブジェクトなので、csv.writerにそのまま渡せます。
    writer = csv.writer(response)
    #データ読み込み
    BookList = BookListModel.objects.all()
    #タイトル行書き込み
    writer.writerow(['No','出版社','書名','著者','価格','詳細','出版年月','ISBN'])
    #データ書き込み
    for BookList in BookList:
        writer.writerow([BookList.id,BookList.publisher,BookList.title,BookList.author,BookList.price, BookList.detail,BookList.date,BookList.isbn])
    return response