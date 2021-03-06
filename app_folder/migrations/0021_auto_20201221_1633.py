# Generated by Django 2.2.7 on 2020-12-21 07:33

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app_folder', '0020_auto_20201219_0237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booklistmodel',
            name='author',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='著者'),
        ),
        migrations.AlterField(
            model_name='booklistmodel',
            name='date',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='出版年月'),
        ),
        migrations.AlterField(
            model_name='booklistmodel',
            name='detail',
            field=models.CharField(blank=True, max_length=10001, null=True, verbose_name='詳細'),
        ),
        migrations.AlterField(
            model_name='booklistmodel',
            name='isbn',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ISBN'),
        ),
        migrations.AlterField(
            model_name='booklistmodel',
            name='price',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='単価'),
        ),
        migrations.AlterField(
            model_name='booklistmodel',
            name='publisher',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='出版社'),
        ),
        migrations.AlterField(
            model_name='disposallistmodel',
            name='author',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='著者'),
        ),
        migrations.AlterField(
            model_name='disposallistmodel',
            name='date',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='発行年'),
        ),
        migrations.AlterField(
            model_name='disposallistmodel',
            name='disposal_date',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 12, 21, 7, 33, 40, 163471, tzinfo=utc), null=True, verbose_name='廃棄日'),
        ),
        migrations.AlterField(
            model_name='disposallistmodel',
            name='isbn',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ISBN'),
        ),
        migrations.AlterField(
            model_name='disposallistmodel',
            name='price',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='本体価格'),
        ),
        migrations.AlterField(
            model_name='disposallistmodel',
            name='publisher',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='出版社'),
        ),
    ]
