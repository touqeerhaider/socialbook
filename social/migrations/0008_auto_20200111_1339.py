# Generated by Django 2.2 on 2020-01-11 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0007_auto_20200107_0048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mypost',
            name='pic',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='myprofile',
            name='pic',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
