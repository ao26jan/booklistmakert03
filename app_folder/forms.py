from django import forms
from .models import BookListModel
from .models import DisposalListModel
from .models import Upload
from django.utils import timezone
from django.core.files.storage import default_storage

class BookRegistForm(forms.ModelForm):
    class Meta:
        model = BookListModel
        fields = '__all__'

class DisposalListForm(forms.ModelForm):
    class Meta:
        model = DisposalListModel
        fields = '__all__'
        MONTHS = {1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'10',11:'11',12:'12'}
        widgets = {
            'reg_date': forms.SelectDateWidget(years=[x for x in range(1990, 2030)],months=MONTHS),
            #'date': forms.SelectDateWidget(years=[x for x in range(1990, 2030)],months=MONTHS),
            'disposal_date': forms.SelectDateWidget(years=[x for x in range(2010, 2030)],months=MONTHS),
        }

class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = '__all__'
