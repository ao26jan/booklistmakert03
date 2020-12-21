'''
リストからレコード削除
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
#from ..forms import BookRegistForm
#from ..forms import DisposalListForm
#from .forms import UploadForm
#from ..search_book import search_book
#from ..img_to_isbn import img_to_isbn
#from PIL import Image,ImageFilter
#from datetime import datetime,date

from . import app_settings
app_settings.init()

def delete_record(request):
    context = app_settings.context
    target_id = request.POST['id']
    target_list = request.POST['list_name']
    if target_list == 'booklist':
        target_record = BookListModel.objects.filter(id = target_id)
    elif target_list == 'disposallist':
        target_record = DisposalListModel.objects.filter(id = target_id)
    target_dict1 = list(target_record.values())
    target_dict = target_dict1[0]
    title = target_dict['title']
    target_record.delete()
    context['booklist'] = BookListModel.objects.all()
    context['disposallist'] = DisposalListModel.objects.all()
    context['message'] = '■「' + title + '」をリストから削除しました。'
    context['ms_flag'] = 1
    #return render(request,'app_folder/index.html',context)
    return redirect('../')