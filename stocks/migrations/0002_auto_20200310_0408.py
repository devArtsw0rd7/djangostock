# Generated by Django 3.0.4 on 2020-03-10 04:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stock',
            old_name='ticker_symbol',
            new_name='ticker',
        ),
    ]