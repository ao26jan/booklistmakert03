'''
app_folder/urlsからの決定を決定をうけて、処理を処理を決定する
'''
import csv
import io
import os
import requests
import json
import shutil
from django import forms
from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from django.views import View,generic
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import BookListModel
from .models import DisposalListModel
#from .models import Upload
from .forms import BookRegistForm
from .forms import DisposalListForm
#from .forms import UploadForm
from .search_book import search_book
from .img_to_isbn import img_to_isbn
from PIL import Image,ImageFilter
from datetime import datetime,date

message = ''
ms_flag = 0
booklist = BookListModel.objects.all()
disposallist = DisposalListModel.objects.all()
bookdata_dict = {}
bookdata_dict_list = []
form = BookRegistForm()
#form_img = UploadForm()
isbn = ""
uploaded_file_url = ""
last_page = ""

#これでhtml内のタグになる
context = {'message':message,
            'ms_flag':ms_flag,
            'booklist':booklist,
            'disposallist':disposallist,
            'bookdata_dict':bookdata_dict,
            'bookdata_dict_list':bookdata_dict_list,
            'form':form,
            #'form_img':form_img,
            'isbn':isbn,
            'uploaded_file_url':uploaded_file_url,
            'last_page':last_page,
            }

#index.htmlにアクセスした場合場合
def index(request):
    global context
    if context['ms_flag'] == 0:
        context['message'] = ""

    context['booklist'] = BookListModel.objects.all()
    context['disposallist'] = DisposalListModel.objects.all()
    context['ms_flag'] = 0
    return render(request, 'app_folder/index.html',context)


#バーコードスキャン
def input_barcode(request):
    global context
    if context['ms_flag'] == 0:
        context['message'] = ""

    #GETのとき（初回表示）初期化

    #POSTで画像がないとき
    if request.method == 'POST' and request.FILES == None:
        context["message"] ="myfileがNULLです。バーコードを撮影、またはバーコード画像を選択してください "
        #return render(request,'app_folder/input_barcode.html',context)
        return redirect ('app_folder/input_barcode.html')

    #POSTで画像があるとき
    elif request.method == 'POST' and request.FILES['myfile']:
        #画像ファイル名取得
        if request.FILES['myfile']:
            myfile = request.FILES['myfile']
        else:
            context["message"] += "画像が読み込めませんでした。画像を再撮影してください"
            return render(request,'app_folder/input_barcode.html',context)

        #画像ファイル取得
        fs = FileSystemStorage()

        #画像ファイル保存とファイル名取得
        filename = fs.save(myfile.name,myfile)

        #ファイルのアドレス取得
        uploaded_file_url = fs.url(filename)
        if uploaded_file_url == None:
            #context["uploaded_file_url"] = uploaded_file_url
            context["message"] = "画像が読み込めませんでした "
            return redirect ('app_folder/input_barcode.html')
            #return render(request,'app_folder/input_barcode.html',context)

        #画像からISBN取得
        image_url = '/home/ao26jan/mysite' + uploaded_file_url
        img = Image.open(image_url)
        isbn = img_to_isbn(img)
        if isbn==None:
            context["message"] = "ISBNが認識できませんでした。再度撮影し直してください"
            os.remove(image_url)
            return render(request,'app_folder/input_barcode.html',context)

        #ISBNから書誌情報取得
        bookdata_dict = search_book(isbn)

        #context["bookdata_dict"] = bookdata_dict
        if bookdata_dict['result'] == 'error':
            context['message'] = "ISBN:" + isbn + " で検索しましたが見つかりませんでした。"
            os.remove(image_url)
            return render(request, 'app_folder/input_barcode.html',context)

        #formにbookdata_dictを差し込み
        form = BookRegistForm(bookdata_dict)
        title = bookdata_dict['title']

        #書籍情報を保存
        if form.is_valid():
            form.save(commit=True) #データ登録
            context['message'] = '■「' + title + '」が登録されました！\n'
            context['ms_flag'] = 1
            context['bookdata_dict'] = bookdata_dict
            context['form'] = form
            os.remove(image_url)
            shutil.rmtree('/home/ao26jan/mysite/media/')
            os.mkdir('/home/ao26jan/mysite/media/')
            return redirect('../')
            #render(request,'app_folder/input_barcode.html',context)
        else:
            #for ele in form:
            #    message = message + "\n" + ele
            context['message'] = '・バリテーションエラーのため登録できませんでした\n'
            context['bookdata_dict'] = bookdata_dict
            context['form'] = form
            #return redirect('../')
            render(request,'app_folder/input_barcode.html',context)

        os.remove(image_url)

    return render(request, 'app_folder/input_barcode.html',context)

#ISBN複数入力
def input_isbns(request):
    global context
    if context['ms_flag'] == 0:
        context['message'] = ""
    '''
    message=""
    booklist = BookListModel.objects.all()
    bookdata_dict = {}
    bookdata_dict_list = []
    form = BookRegistForm()
    isbn = ""
    isbn_list=[]
    i_list=[]
    len_isbn_list = 0
    context= {'message':message,
        'booklist':booklist,
        'bookdata_dict':bookdata_dict,
        'bookdata_dict_list':bookdata_dict_list,
        'form':form,
        'isbn':isbn,
        'isbn_list':isbn_list,
        'i_list':i_list,
        'len_isbn_list':len_isbn_list,
        }
    '''
    #context["message"]="ISBNを978から入力してください"
    #booklist = BookListModel.objects.all()
    if request.method == 'POST':
    # 画面からPOSTした場合
        isbns = request.POST['isbns']
        isbn_list=isbns.split()

        len_isbn_list = len(isbn_list)
        context["len_isbn_list"]=len_isbn_list

        context["isbn_list"]=isbn_list
        for isbn in isbn_list:

            context["i_list"]=i_list

            bookdata_dict = {}
            #isbn = isbn_list[i]
            context["isbn"]=isbn
            bookdata_dict = search_book(isbn)

            bookdata_dict_list.append(bookdata_dict)
            context["bookdata_dict_list"]=bookdata_dict_list

            #bookdata_json = json.dumps(bookdata_dict) #JSONに変換
            #formにPOSTデータ書き込み。しないとバリテーションエラー
            #form = BookRegistForm(request.POST)

            #formにbookdata_dictを差し込み
            form = BookRegistForm(bookdata_dict)
            #return HttpResponse(form['publisher'])

            # formを保存
            if form.is_valid():
                form.save(commit=True) #データ登録
                context['message'] = '■データが登録されました！\n'
                context['bookdata_dict']=bookdata_dict
                context['form']=form
            else:
                #for ele in form:
                #    message = message + "\n" + ele
                context['message'] = '・バリテーションエラーのため登録できませんでした'
                context['bookdata_dict']=bookdata_dict
                context['form']=form
        return redirect('../')
    return render(request, 'app_folder/input_isbns.html',context)


#ISBN入力
def input_isbn(request):
    global context
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
            return render(request, 'app_folder/input_isbn.html',context)

        #bookdata_json = json.dumps(bookdata_dict) #JSONに変換
        #formにPOSTデータ書き込み。しないとバリテーションエラー
        form = BookRegistForm(request.POST)
        #formにbookdata_dictを差し込み
        form = BookRegistForm(bookdata_dict)
        #return HttpResponse(form['publisher'])
        title = bookdata_dict['title']

        # 画面からPOSTした値を取得
        if form.is_valid():
            form.save(commit=True) #データ登録
            context['message'] = '■「' + title + '」が登録されました！\n'
            context['ms_flag'] = 1
            context['bookdata_dict']=bookdata_dict
            context['form']=form
            return redirect('../')
            #return render(request, '../app_folder/index.html',context)
        else:
            #for ele in form:
            #    message = message + "\n" + ele
            context['message'] = '■バリテーションエラーのため登録できませんでした'
            context['ms_flag'] = 1
            context['bookdata_dict'] = bookdata_dict
            context['form'] = form
            #return redirect('../')
            return render(request, 'app_folder/input_isbn.html',context)

    return render(request, 'app_folder/input_isbn.html',context)

#手入力用関数
def input_manual(request):
    global context
    if context['ms_flag'] == 0:
        context['message'] = ""
    form = BookRegistForm() # formのインスタンス作成

    if request.method == 'POST':
    # 画面からPOSTした場合に、実行される
        form = BookRegistForm(request.POST)
        title = ""
        # 画面からPOSTした値を取得
        if form.is_valid():
            form.save(commit=True) #データが登録される
            context['message'] = '■「' + title +'」が登録されました！\n'
            context['ms_flag'] = 1
            return redirect('../')
            #return render(request, 'app_folder/index.html',context)
        else:
            context['message'] = "再入力してください"
            context['ms_flag'] = 0
            return render(request,'app_folder/input_manual.html',context)

    # POSTでない場合の画面にformを渡す
    return render(request, 'app_folder/input_manual.html', {'form': form})

#ISBN入力
def disposal_isbn(request):
    global context
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
        form = DisposalListForm(request.POST)
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
            context['message'] += '■「' + title + '」が見つかりました。\n'
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

def disposal_barcode(request):
    global context

    #POSTで画像がないとき
    if request.method == 'POST' and request.FILES == None:
        context["message"] ="myfileがNULLです。バーコードを撮影、またはバーコード画像を選択してください "
        #return render(request,'app_folder/disposal_barcode.html',context)
        return redirect ('app_folder/disposal_barcode.html')

    #POSTで画像があるとき
    elif request.method == 'POST' and request.FILES['myfile']:
        #画像ファイル名取得
        if request.FILES['myfile']:
            myfile = request.FILES['myfile']
        else:
            context["message"] += "画像が読み込めませんでした。画像を再撮影してください"
            return render(request,'app_folder/disposal_barcode.html',context)

        #画像ファイル取得
        fs = FileSystemStorage()

        #画像ファイル保存とファイル名取得
        filename = fs.save(myfile.name,myfile)

        #ファイルのアドレス取得
        uploaded_file_url = fs.url(filename)
        if uploaded_file_url == None:
            #context["uploaded_file_url"] = uploaded_file_url
            context["message"] = "画像が読み込めませんでした "
            return redirect ('app_folder/disposal_barcode.html')
            #return render(request,'app_folder/disposal_barcode.html',context)

        #画像からISBN取得
        image_url = '/home/ao26jan/mysite' + uploaded_file_url
        img = Image.open(image_url)
        isbn = img_to_isbn(img)
        if isbn==None:
            context["message"] = "ISBNが認識できませんでした。再度撮影し直してください"
            os.remove(image_url)
            return render(request,'app_folder/disposal_barcode.html',context)

        #ISBNから書誌情報取得
        bookdata_dict = search_book(isbn)

        #context["bookdata_dict"] = bookdata_dict
        if bookdata_dict['result'] == 'error':
            context['message'] = "ISBN:" + isbn + " で検索しましたが見つかりませんでした。"
            os.remove(image_url)
            return render(request, 'app_folder/disposal_barcode.html',context)

        #formにbookdata_dictを差し込み
        form = DisposalListForm(bookdata_dict)
        title = bookdata_dict['title']
        title = form['title'].value()

        #書籍情報を保存
        if form.is_valid():
            #form.save(commit=True) #データ登録
            context['message'] += '■「' + title + '」が廃棄リストに登録されました！\n'
            context['ms_flag'] = 1
            context['bookdata_dict'] = bookdata_dict
            context['form'] = form
            os.remove(image_url)
            shutil.rmtree('/home/ao26jan/mysite/media/')
            os.mkdir('/home/ao26jan/mysite/media/')
            context['last_page'] = 'disposal_barcode'
            #return redirect('../')
            return render(request,'app_folder/disposal_manual.html',context)
        else:
            #for ele in form:
            #    message = message + "\n" + ele
            context['message'] = '・バリテーションエラーのため登録できませんでした\n'
            context['bookdata_dict'] = bookdata_dict
            context['form'] = form
            #return redirect('../')
            return render(request,'app_folder/disposal_barcode.html',context)

        #os.remove(image_url)

    return render(request, 'app_folder/disposal_barcode.html',context)

#手入力用関数
def disposal_manual(request):
    global context
    if context['ms_flag'] == 0:
        context['message'] = ""

    #POSTでないとき
    if request.method != 'POST':
        #barcodeから来たとき
        if context['last_page'] == 'disposal_barcode':
            #form = context['form']
            #form = DisposalListForm(request.POST)
            context['last_page'] = 'disposal_manual'
            context['message'] = 'あなたはbarcodeからきましたね？'
            context['ms_flag'] = 1
        #トップページからきた時
        else:
            form = DisposalListForm() # formのインスタンス作成
            context['message'] = 'POSTではありませんでした'
            context['ms_flag'] = 1
            context['form'] = form
            context['last_page'] = 'disposal_manual'

    # POST=登録ボタンがおされた時
    elif request.method == 'POST':
        form = DisposalListForm(request.POST)
        if form.is_valid():
            #bookdata_dict = context['bookdata_dict']
            title = '' #form['title']
            form.save(commit=True) #データが登録される
            context['message'] = '■「' + title +'」が登録されました！\n'
            context['ms_flag'] = 1
            context['last_page'] = 'disposal_manual'
            return redirect('../')
            #return render(request, 'app_folder/index.html',context)
        else:
            context['message'] = "バリテーションエラー。再入力してください"
            context['ms_flag'] = 1
            context['last_page'] = 'disposal_manual'
            return render(request,'app_folder/disposal_manual.html',context)

    context['ms_flag'] = 0
    return render(request, 'app_folder/disposal_manual.html', context)

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

#発注リスト全件削除
def delete_all(request):
    booklist = BookListModel.objects.all()
    booklist.delete()
    context['message'] = '発注リストを全件削除しました。'
    context['ms_flag'] = 1
    context['booklist'] = BookListModel.objects.all()
    #return render(request,'app_folder/index.html',context)
    return redirect('../')

#廃棄リスト全件削除
def delete_disposal(request):
    disposallist = DisposalListModel.objects.all()
    disposallist.delete()
    context['message'] = '廃棄リストを全件削除しました。'
    context['ms_flag'] = 1
    context['disposallist'] = DisposalListModel.objects.all()
    #return render(request,'app_folder/index.html',context)
    return redirect('../')

#１件削除
def delete_record(request):
    global context
    target_id = request.POST['id']
    target_list = request.POST['list_name']
    if target_list == 'booklist':
        target_record = BookListModel.objects.filter(id = target_id)
    elif target_list == 'disposallist':
        target_record = DisposalListModel.objects.filter(id = target_id)
    title = ''#target_record['title']
    target_record.delete()
    context['booklist'] = BookListModel.objects.all()
    context['disposallist'] = DisposalListModel.objects.all()
    context['message'] = '■「' + title + '」をリストから削除しました。'
    context['ms_flag'] = 1
    #return render(request,'app_folder/index.html',context)
    return redirect('../')


