'''
app_folder/urlsからの決定を決定をうけて、処理を処理を決定する
'''
import csv
import io
import requests
import json
from django import forms
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.http import HttpResponse
from .models import BookListModel
from .forms import BookRegistForm
from .search_book import search_book

message = 'start!'
booklist = BookListModel.objects.all()
bookdata_dict = {}
form = BookRegistForm()

context = {'message':message,
            'booklist':booklist,
            'bookdata_dict':bookdata_dict,
            'form':form,
            }

def index(request):
    context['booklist'] = BookListModel.objects.all()
    return render(request, 'app_folder/index.html',context)

#ISBN入力
def input_isbn(request):
    booklist = BookListModel.objects.all()
    if request.method == 'POST':
    # 画面からPOSTした場合
        isbn = request.POST['isbn']
        bookdata_dict = search_book(isbn)
        #bookdata_json = json.dumps(bookdata_dict)
        #formにPOSTデータ書き込み。しないとバリテーションエラー
        form = BookRegistForm(request.POST)
        #formにbookdata_dictを差し込み
        form = BookRegistForm(bookdata_dict)
        #form_type = type(form['publisher'])
        #return HttpResponse(form_type)
        #form['publisher'] = '阪急コミュニケーションズ' #bookdata_dict['出版社']
        #return redirect('../')
        #form = BookListModel.objects.all()
        #return HttpResponse(form['publisher'])

        # 画面からPOSTした値を取得
        if form.is_valid():
            form.save(commit=True) #データ登録
            context['message'] = 'search and save is successed!\n'
            context['bookdata_dict']=bookdata_dict
            context['form']=form
            return redirect('../')
            #return render(request, '../app_folder/index.html',context)
        else:
            #for ele in form:
            #    message = message + "\n" + ele
            context['message'] = 'valid error'
            context['bookdata_dict']=bookdata_dict
            context['form']=form
            return redirect('../')
            #return render(request, '../app_folder/index.html',context)

    return render(request, 'app_folder/input_isbn.html')

#手入力用関数
def input_manual(request):

    form = BookRegistForm() # formのインスタンス作成

    if request.method == 'POST':
    # 画面からPOSTした場合に、実行される
        form = BookRegistForm(request.POST)
        # 画面からPOSTした値を取得
        if form.is_valid():
            form.save(commit=True) #データが登録される
            message = 'データが登録されました！\n'
            return redirect('../')
            #return render(request, 'app_folder/index.html')
        else:
            message = "再入力してください"
            return redirect('app_folder/input_manual.html')

    # POSTでない場合の画面にformを渡す
    return render(request, 'app_folder/input_manual.html', {'form': form})

#ファイル出力
def csv_export(request):
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

#全件削除
def delete_all(request):
    booklist = BookListModel.objects.all()
    booklist.delete()
    return redirect('../')
