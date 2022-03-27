# Generated by Django 4.0.3 on 2022-03-25 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('madrasaticApp', '0003_remove_myuser_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='img',
            field=models.ImageField(default='/madrasatic/media/defaultuser.png', upload_to=None),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='role',
            field=models.CharField(choices=[('Utilisateur', 'User'), ('Responsable', 'Responsable'), ('Admin', 'Admin')], default=('Utilisateur', 'User'), max_length=30),
        ),
    ]
