# Generated by Django 2.1.1 on 2018-10-09 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='pub_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='updated',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
