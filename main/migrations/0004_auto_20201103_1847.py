# Generated by Django 3.1.3 on 2020-11-03 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20201103_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
