'''
ブラウザからのhttpリクエストを受けて、
どのview関数で処理するか決定する
'''

from django.urls import path
from . import views

app_name = 'app_folder'
urlpatterns = [
    path('', views.index, name='index'),
    path('input_isbn/', views.input_isbn, name='input_isbn'),
    path('input_manual/', views.input_manual, name='input_manual'),
    path('csv_export/', views.csv_export, name='csv_export'),
    path('delete_all/', views.delete_all, name='delete_all'),
]