'''
トップページindex.html生成
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
from ..models import BookListModel
from ..models import DisposalListModel
#from .models import Upload
from ..forms import BookRegistForm
#from ..forms import DisposalListForm
#from ..forms import UploadForm
#from .search_book import search_book
#from .img_to_isbn import img_to_isbn
#from PIL import Image,ImageFilter

from . import app_settings
app_settings.init()

#index.htmlにアクセスした場合
def index(request):
    #global context
    context = app_settings.context

    if context['ms_flag'] == 0:
        context['message'] = ""
    context['booklist'] = BookListModel.objects.all()
    context['disposallist'] = DisposalListModel.objects.all()
    bookdata_dict = {}
    bookdata_dict_list = []
    form = BookRegistForm()
    isbn = ""
    uploaded_file_url = ""
    last_page = "index"
    i_list = ""
    mode = ""
    target_id = 0
    target_record = ""
    count_success = 0
    count_data = 0
    isbn_list = []

    context['ms_flag'] = 0
    return render(request, 'app_folder/index.html',context)