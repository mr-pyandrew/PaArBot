# Generated by Django 3.2.15 on 2022-10-05 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0008_bearing2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaf',
            name='leaf',
            field=models.CharField(max_length=512, verbose_name='Категория'),
        ),
    ]