# Generated by Django 4.0.3 on 2022-03-21 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('madrasaticApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='img',
            field=models.ImageField(default='no img', upload_to=None),
        ),
    ]