# Generated by Django 4.0.4 on 2022-04-22 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_userprofile_image_alter_article_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='description',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
