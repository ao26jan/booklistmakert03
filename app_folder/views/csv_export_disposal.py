'''
廃棄リストを出力する
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
#from ..models import BookListModel
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
def csv_export_disposal(request):
    #context=app_settings.context
    response = HttpResponse(content_type='text/csv')
    #ファイル名設定
    response['Content-Disposition'] = 'attachment; filename="disposallist.csv"'
    # HttpResponseオブジェクトはファイルっぽいオブジェクトなので、csv.writerにそのまま渡せます。
    writer = csv.writer(response)
    #データ読み込み
    DisposalList = DisposalListModel.objects.all()
    #タイトル行書き込み
    writer.writerow(['受入日','登録番号','著者','書名','出版社','本体価格','発行年','分類番号','廃棄日','備考'])
    #データ書き込み
    for DisposalList in DisposalList:
        writer.writerow([DisposalList.reg_date,DisposalList.reg_no,DisposalList.author,DisposalList.title,DisposalList.publisher,DisposalList.price, DisposalList.date,DisposalList.class_no,DisposalList.disposal_date,DisposalList.remarks])
    return response