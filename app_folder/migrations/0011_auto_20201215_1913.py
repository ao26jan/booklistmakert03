# Generated by Django 2.2.7 on 2020-12-15 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_folder', '0010_auto_20201215_1829'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='images')),
                ('filename', models.CharField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='Book',
        ),
    ]
