# Generated by Django 4.2.9 on 2024-09-16 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0005_producto_informacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalleventa',
            name='subtotal',
            field=models.IntegerField(default=0),
        ),
    ]
