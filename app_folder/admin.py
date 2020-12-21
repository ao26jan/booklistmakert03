from django.contrib import admin
from .models import BookListModel
from .models import DisposalListModel
#from .models import Upload

admin.site.register(BookListModel)
admin.site.register(DisposalListModel)
#admin.site.register(Upload)
