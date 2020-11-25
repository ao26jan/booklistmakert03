from django.db import models

class BookListModel(models.Model):
    publisher = models.CharField('出版社',max_length=255)
    title = models.CharField('書名',max_length=255)
    author = models.CharField('著者',max_length=255)
    price = models.CharField('単価',max_length=255)
    detail = models.CharField('詳細',max_length=10001)
    date = models.CharField('出版年月',max_length=255)
    isbn = models.CharField('ISBN',max_length=255,unique=True)

    def __str__(self):
        return self.title

'''
class SampleDB(models.Model):
    class Meta:
        db_table = 'sample_table' # DB内で使用するテーブル名
        verbose_name_plural = 'sample_table' # Admionサイトで表示するテーブル名
    sample1 = models.IntegerField('sample1', null=True, blank=True) # 数値を格納
    sample2 = models.CharField('sample2', max_length=255, null=True, blank=True) # 文字列を格納
'''