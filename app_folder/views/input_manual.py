'''
発注リストを手入力
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
from ..models import BookListModel
#from ..models import DisposalListModel
#from .models import Upload
from ..forms import BookRegistForm
#from ..forms import DisposalListForm
#from ..forms import UploadForm
#from ..search_book import search_book
#from ..img_to_isbn import img_to_isbn
#from PIL import Image,ImageFilter
from django.shortcuts import get_object_or_404

from . import app_settings
app_settings.init()

#手入力用関数
def input_manual(request):
    context = app_settings.context
    if context['ms_flag'] == 0:
        context['message'] = ""
    form = BookRegistForm() # formのインスタンス作成

    # POSTの場合
    if request.method == 'POST':

        #編集モードのとき
        if context['mode'] == 'edit':
            #request.POST['id'] = context['target_id']
            #target_record = context['target_record']#更新前の対象レコード：クエリ形式
            id = context['target_id']
            target_record =  get_object_or_404(BookListModel,pk=id)
            title = ""
            form = BookRegistForm(request.POST,instance=target_record)#更新された情報：フォーム形式
            context['form'] = form
            # 画面からPOSTした値を取得
            if form.is_valid():
                form.save(commit=True) #データ更新
                #target_record.save()#データ更新
                context['message'] = '■「' + title +'」を更新しました。\n'
                context['ms_flag'] = 1
                context['mode'] = ''
                return redirect('../')
                #return render(request, 'app_folder/index.html',context)
            else:
                context['message'] = "■必須項目が未入力または書式エラーです。再入力してください"
                context['ms_flag'] = 0
                return render(request,'app_folder/input_manual.html',context)

        #編集モードではない時
        else:
            #トップ画面の手入力から来た場合
            if request.POST['input_method'] == 'manual':
                context['form'] = BookRegistForm()

            #登録ボタンを押して来た時
            elif request.POST['input_method'] == 'regist':
                form = BookRegistForm(request.POST)
                title = ""
                context['form'] = form
                # 画面からPOSTした値を取得
                if form.is_valid():
                    form.save(commit=True) #データが登録される
                    context['message'] = '■「' + title +'」が登録されました！\n'
                    context['ms_flag'] = 1
                    return redirect('../')
                    #return render(request, 'app_folder/index.html',context)
                else:
                    context['message'] = "■バリテーションエラー：再入力してください"
                    context['ms_flag'] = 0
                    return render(request,'app_folder/input_manual.html',context)

            #編集ボタンを押してきた時、編集モードに設定
            elif request.POST['input_method'] == 'edit':
                target_id = request.POST['id']
                context['target_id'] = target_id
                target_queryset = BookListModel.objects.filter(id = target_id)
                context['target_record'] = target_queryset
                target_dict = list(target_queryset.values())
                form = BookRegistForm(target_dict[0])
                #context['message'] = target_dict[0]
                context['form'] = form
                context['mode'] = 'edit'


    # POSTでない場合の画面にformを渡す
    return render(request, 'app_folder/input_manual.html', context)