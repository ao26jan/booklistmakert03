from django import forms
from .models import BookListModel

class BookRegistForm(forms.ModelForm):
    class Meta:
        model = BookListModel
        # モデルのインスタンスを生成

        fields = '__all__'
        # fieldsに__all__をセットすると、モデル内の全てのフィールドが用いられる

        '''
        fields = ('publisher', 'title','author','price','detail','date','isbn')
        labels = {
            'publisher': '出版社',
            'title': '書名',
            'author':'著者',
            'price':'単価',
            'detail':'詳細',
            'date':'出版年月',
            'isbn':'ISBN',
        }
        '''