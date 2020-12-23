'''
廃棄リストに手入力で追加
'''
#import csv
#import io
#import os
#import requests
#import json
#import shutil
#from django import forms
from django.shortcuts import render
from django.shortcuts import redirect
#from django.conf import settings
#from django.views import View,generic
#from django.http import HttpResponse
#from django.core.files.storage import FileSystemStorage
#from ..models import BookListModel
from ..models import DisposalListModel
#from ..models import Upload
#from ..forms import BookRegistForm
from ..forms import DisposalListForm
#from ..forms import UploadForm
#from ..search_book import search_book
#from ..img_to_isbn import img_to_isbn
#from PIL import Image,ImageFilter
#from datetime import datetime,date
from django.shortcuts import get_object_or_404

from . import app_settings
app_settings.init()

#手入力用関数
def disposal_manual(request):
    context = app_settings.context
    if context['ms_flag'] == 0:
        context['message'] = ""

    #POSTでないbarcodeまたはindexからきたとき
    if request.method != 'POST':
        #barcodeから来たとき
        if context['last_page'] == 'disposal_barcode':
            #form = context['form']
            #form = DisposalListForm(request.POST)
            #context['message'] = 'あなたはbarcodeからきましたね？ NOT_POST'
            #context['ms_flag'] = 1
            context['last_page'] = 'disposal_manual'
            context['mode'] = 'new'
        #トップページからきた時
        else:
            form = DisposalListForm() # formのインスタンス作成
            context['form'] = form
            #context['message'] = 'トップページからきましたね？ NOT_POST'
            #context['ms_flag'] = 1
            context['last_page'] = 'disposal_manual'
            context['mode'] = 'new'

    # POST=登録または編集ボタンがおされた時
    elif request.method == 'POST':

        #編集を押してきた時
        if request.POST['input_method'] == 'edit':
            target_id = request.POST['id']
            context['target_id'] = target_id
            target_queryset = DisposalListModel.objects.filter(id = target_id)
            context['target_record'] = target_queryset
            target_dict = list(target_queryset.values())
            form = DisposalListForm(target_dict[0])
            #context['message'] = target_dict[0]
            context['form'] = form
            context['mode'] = 'edit'

        #POST&登録を押してきた時
        else:
            #編集モードなら
            if context['mode'] == 'edit':
                id = context['target_id']
                target_record =  get_object_or_404(DisposalListModel,pk=id)
                form = DisposalListForm(request.POST,instance=target_record)#更新された情報：フォーム形式
                context['form'] = form

                #form = DisposalListForm(request.POST)
                if form.is_valid():
                    form.save(commit=True) #データが登録される
                    #bookdata_dict = context['bookdata_dict']
                    title1 = request.POST['title']
                    #title2 = title1[0]
                    #title = title2['title']
                    title = title1
                    context['message'] += '■「' + title +'」が登録されました。\n'
                    context['ms_flag'] = 1
                    context['last_page'] = 'disposal_manual'
                    context['mode'] = ''
                    return redirect('../')
                    #return render(request, 'app_folder/index.html',context)
                else:
                    context['message'] = "■必須項目が未入力、または書式エラーです。再入力してください"
                    context['ms_flag'] = 1
                    context['last_page'] = 'disposal_manual'
                    return render(request,'app_folder/disposal_manual.html',context)
            #編集モードでない時＝通常の登録なら
            else:
                form = DisposalListForm(request.POST)
                context['form'] = form
                if form.is_valid():
                    form.save(commit=True)
                    title1 = request.POST['title']
                    #title2 = title1[0]
                    #title = title2['title']
                    title = title1
                    context['message'] = '■「' + title +'」が登録されました。\n'
                    context['ms_flag'] = 1
                    return redirect('../')
                    #return render(request, 'app_folder/index.html',context)
                else:
                    context['message'] = "■必須項目が未入力、または書式エラーです。再入力してください。"
                    context['ms_flag'] = 0
                    return render(request,'app_folder/disposal_manual.html',context)

    context['ms_flag'] = 0
    return render(request, 'app_folder/disposal_manual.html', context)