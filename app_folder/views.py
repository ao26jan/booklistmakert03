'''
app_folder/urlsからの決定を決定をうけて、処理を処理を決定する
'''
import csv
import io
import requests
from django import forms
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.http import HttpResponse
from .models import BookListModel
from .forms import BookRegistForm
from .search_book import search_book

def index(request):
    booklist = BookListModel.objects.all()
    return render(request, 'app_folder/index.html',{'booklist':booklist})

def input_isbn(request):

    if request.method == 'POST':
    # 画面からPOSTした場合
        isbn = request.POST['isbn']
        #isbn = isbn
        bookdata_dict = search_book(isbn)

        #return HttpResponse(bookdata)

        #formにbookdata_dictを差し込み
        form = BookRegistForm()
        #form_type = type(form['publisher'])
        #return HttpResponse(form_type)
        #form['publisher']
        pub = bookdata_dict['出版社']
        #return redirect('../')

        #form = BookListModel.objects.all()
        return HttpResponse(type(pub))

        # 画面からPOSTした値を取得
        if form.is_valid():
            form.save(commit=True) #データが登録される
            return redirect('../')
            #return render(request, 'app_folder/index.html')
        else:
            print('ERROR FORM INVALID')


    return render(request, 'app_folder/input_isbn.html')


def input_manual(request):
    # form登録用のビュー

    '''
    params = {'message': '', 'form': None}
    if request.method == 'POST':
        form = NewBookForm(request.POST)
        if form.is_valid():
            form.save()
            return index(request)#redirect('list')
        else:
            params['message'] = '再入力して下さい'
            params['form'] = form
    else:
        params['form'] = NewBookForm()
    return render(request, 'app_folder/input_manual.html', params)
    '''

    form = BookRegistForm() # formのインスタンス作成

    if request.method == 'POST':
    # 画面からPOSTした場合に、実行される
        form = BookRegistForm(request.POST)
        # 画面からPOSTした値を取得
        if form.is_valid():
            form.save(commit=True) #データが登録される
            return redirect('../')
            #return render(request, 'app_folder/index.html')
        else:
            print('ERROR FORM INVALID')

    return render(request, 'app_folder/input_manual.html', {'form': form})
    # POSTでない場合の画面にformを渡す

    '''
    フォームで送受信する場合
    def post(self, request, *args, **kwargs):
        context = {
            'isbn': request.POST['isbn'],
        }
        return render(request, 'index.html', context)
    '''

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
        writer.writerow([BookList.id,BookList.publisher,BookList.title,BookList.author,BookList.price, BookList.detail,BookList.pubdate,BookList.isbn])
    return response

#全件削除
def delete_all(request):
    booklist = BookListModel.objects.all()
    booklist.delete()
    return redirect('../')
