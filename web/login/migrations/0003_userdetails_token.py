# Generated by Django 3.0 on 2020-02-11 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20200210_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='token',
            field=models.CharField(default='NULL', max_length=100),
            preserve_default=False,
        ),
    ]
