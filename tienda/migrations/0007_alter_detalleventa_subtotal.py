# Generated by Django 4.2.9 on 2024-09-16 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0006_detalleventa_subtotal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalleventa',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
