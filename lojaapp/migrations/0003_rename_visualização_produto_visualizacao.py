# Generated by Django 4.1.1 on 2022-09-28 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lojaapp', '0002_alter_cliente_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='produto',
            old_name='visualização',
            new_name='visualizacao',
        ),
    ]
