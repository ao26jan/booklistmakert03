'''
views.pyに代わりviewsフォルダを設定
'''

#グローバル変数設定
from . import app_settings
app_settings.init()

from .csv_export import *
from .delete_all import *
from .delete_disposal import *
from .delete_record import *
from .disposal_barcode import *
from .disposal_isbn import *
from .disposal_manual import *
from .index import *
from .input_barcode import *
from .input_isbn import *
from .input_isbns import *
from .input_manual import *