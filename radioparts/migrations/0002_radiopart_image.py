# Generated by Django 4.2.4 on 2023-08-20 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('radioparts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='radiopart',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='radio_parts/'),
        ),
    ]
