# Generated by Django 3.2.15 on 2022-09-30 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0005_alter_bearing_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='bearing',
            name='photo',
            field=models.ImageField(null=True, upload_to='media/images', verbose_name='Картинка'),
        ),
    ]
