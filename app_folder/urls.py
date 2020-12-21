'''
ブラウザからのhttpリクエストを受けて、
どのview関数で処理するか決定する
'''

from django.urls import path
#from . import views
from .views.csv_export import *
from .views.csv_export_disposal import *
from .views.delete_all import *
from .views.delete_disposal import *
from .views.delete_record import *
from .views.disposal_barcode import *
from .views.disposal_isbn import *
from .views.disposal_manual import *
from .views.index import *
from .views.input_barcode import *
from .views.input_isbn import *
from .views.input_isbns import *
from .views.input_manual import *


app_name = 'app_folder'
urlpatterns = [
    path('', index, name='index'),
    path('input_barcode/', input_barcode, name='input_barcode'),
    path('input_isbn/', input_isbn, name='input_isbn'),
    path('input_isbns/', input_isbns, name='input_isbns'),
    path('input_manual/', input_manual, name='input_manual'),
    path('disposal_isbn/', disposal_isbn, name='disposal_isbn'),
    path('disposal_barcode/', disposal_barcode, name='disposal_barcode'),
    path('disposal_manual/', disposal_manual, name='disposal_manual'),
    path('csv_export/', csv_export, name='csv_export'),
    path('csv_export_disposal/', csv_export_disposal, name='csv_export_disposal'),
    path('delete_all/', delete_all, name='delete_all'),
    path('delete_disposal/', delete_disposal, name='delete_disposal'),
    path('delete_record/', delete_record, name='delete_record'),
]