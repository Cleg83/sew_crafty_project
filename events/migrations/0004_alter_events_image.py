# Generated by Django 5.1.4 on 2025-02-05 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_remove_events_image_url_alter_events_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='image',
            field=models.ImageField(default='no-image.svg', upload_to=''),
        ),
    ]
