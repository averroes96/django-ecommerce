# Generated by Django 3.2.10 on 2022-01-01 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='email',
            new_name='digital',
        ),
    ]
