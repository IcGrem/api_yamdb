# Generated by Django 2.2.6 on 2020-06-12 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20200612_0101'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deletedcategories',
            old_name='name',
            new_name='delname',
        ),
        migrations.RenameField(
            model_name='deletedcategories',
            old_name='slug',
            new_name='delslug',
        ),
    ]
