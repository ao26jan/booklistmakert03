# Generated by Django 2.2.7 on 2020-12-21 16:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app_folder', '0022_auto_20201222_0110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booklistmodel',
            name='price',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='本体価格（税抜）'),
        ),
        migrations.AlterField(
            model_name='disposallistmodel',
            name='disposal_date',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 12, 21, 16, 14, 34, 268389, tzinfo=utc), null=True, verbose_name='廃棄日'),
        ),
        migrations.AlterField(
            model_name='disposallistmodel',
            name='price',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='本体価格（税抜）'),
        ),
    ]
