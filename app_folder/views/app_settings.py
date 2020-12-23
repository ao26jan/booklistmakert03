'''
グローバル変数定義
'''

from ..forms import BookRegistForm
from ..forms import DisposalListForm
from ..models import BookListModel
from ..models import DisposalListModel

def init():
    global context
    #これでhtml内のタグ（テンプレート言語）になる
    context = {'message':"",
                'ms_flag':0,
                'booklist':BookListModel.objects.all(),
                'disposallist':DisposalListModel.objects.all(),
                'bookdata_dict':{},
                'bookdata_dict_list':[],
                'form':BookRegistForm(),
                #'form_img':form_img,
                'isbn':"",
                'uploaded_file_url':"",
                'last_page':"",
                'i_list':"",
                'mode':"",
                'target_id':0,
                'target_record':"",
                'count_success':0,
                'count_data':0,
                'isbn_list':[],
                }