# Generated by Django 2.1.1 on 2018-10-09 20:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import home.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0002_auto_20181009_1445'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Author',
        ),
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-timestamp', '-updated']},
        ),
        migrations.RenameField(
            model_name='article',
            old_name='article_height',
            new_name='height_field',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='article_width',
            new_name='width_field',
        ),
        migrations.RemoveField(
            model_name='article',
            name='headline',
        ),
        migrations.RemoveField(
            model_name='article',
            name='pub_date',
        ),
        migrations.AddField(
            model_name='article',
            name='content',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, height_field='heigth_field', null=True, upload_to=home.models.upload_location, width_field='width_field'),
        ),
        migrations.AddField(
            model_name='article',
            name='publish',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='title',
            field=models.CharField(default=django.utils.timezone.now, max_length=120),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='article',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
