# Generated by Django 4.1.2 on 2022-10-18 23:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lojaapp', '0007_alter_pedido_order_carro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carro',
            name='cliente',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='lojaapp.cliente'),
            preserve_default=False,
        ),
    ]
