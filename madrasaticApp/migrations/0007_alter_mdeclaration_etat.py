# Generated by Django 4.0.3 on 2022-05-03 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('madrasaticApp', '0006_alter_mdeclaration_etat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mdeclaration',
            name='etat',
            field=models.CharField(choices=[('brouillon', 'Brouillon'), ('publiée', 'Publiée'), ('non traitée', 'non traitée'), ('en cours de traitement', 'en cours de traitement'), ('traitée', 'traitée')], default='brouillon', max_length=150),
        ),
    ]
