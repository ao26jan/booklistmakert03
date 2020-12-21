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
#from django.shortcuts import render
from django.shortcuts import redirect
#from django.conf import settings
#from django.views import View,generic
#from django.http import HttpResponse
#from django.core.files.storage import FileSystemStorage
from ..models import BookListModel
from ..models import DisposalListModel
#from .models import Upload
#from .forms import BookRegistForm
#from .forms import DisposalListForm
#from .forms import UploadForm
#from .search_book import search_book
#from .img_to_isbn import img_to_isbn
#from PIL import Image,ImageFilter
#from datetime import datetime,date

from . import app_settings
app_settings.init()

#発注リスト全件削除
def delete_all(request):
    context=app_settings.context
    booklist = BookListModel.objects.all()
    booklist.delete()
    context['message'] = '■発注リストを全件削除しました。'
    context['ms_flag'] = 1
    context['booklist'] = BookListModel.objects.all()
    #return render(request,'app_folder/index.html',context)
    return redirect('../')