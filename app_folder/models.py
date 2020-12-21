from django.db import models
from django.utils import timezone

class BookListModel(models.Model):
    publisher = models.CharField('出版社',max_length=255,blank=True, null=True)
    title = models.CharField('書名',max_length=255)
    author = models.CharField('著者',max_length=255,blank=True, null=True)
    price = models.CharField('単価',max_length=255,blank=True, null=True)
    detail = models.CharField('詳細',max_length=10001,blank=True, null=True)
    date = models.CharField('出版年',max_length=4,blank=True, null=True)
    isbn = models.CharField('ISBN',max_length=13,blank=True, null=True)
    def __str__(self):
        return self.title

class DisposalListModel(models.Model):
    reg_date = models.DateField('受入日',blank=True, null=True)
    reg_no = models.CharField('登録番号',max_length=255,blank=True, null=True)
    author = models.CharField('著者',max_length=255,blank=True, null=True)
    title = models.CharField('書名',max_length=255)
    publisher = models.CharField('出版社',max_length=255,blank=True, null=True)
    price = models.CharField('本体価格',max_length=255,blank=True, null=True)
    date = models.CharField('発行年',max_length=4,blank=True, null=True)
    class_no = models.CharField('分類番号',max_length=255,blank=True, null=True)
    disposal_date = models.DateField('廃棄日',blank=True, null=True,default=timezone.now())
    remarks = models.CharField('備考',max_length=10001,blank=True, null=True)
    isbn = models.CharField('ISBN',max_length=13,blank=True, null=True)
    def __str__(self):
        return self.title

class Upload(models.Model):
    file = models.CharField('url',max_length=100)
    description = models.CharField('詳細',max_length=255)
    def __str__(self):
        return self.title