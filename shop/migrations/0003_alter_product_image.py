# Generated by Django 5.1.4 on 2025-01-20 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_product_permanently_unavailable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='no-image.svg', upload_to=''),
        ),
    ]
