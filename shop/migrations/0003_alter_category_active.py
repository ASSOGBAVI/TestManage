# Generated by Django 3.2.5 on 2023-09-06 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_product_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
