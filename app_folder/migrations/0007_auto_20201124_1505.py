# Generated by Django 2.2.7 on 2020-11-24 06:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_folder', '0006_memo'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BookListDB',
            new_name='BookListModel',
        ),
        migrations.DeleteModel(
            name='Memo',
        ),
        migrations.DeleteModel(
            name='SampleDB',
        ),
    ]