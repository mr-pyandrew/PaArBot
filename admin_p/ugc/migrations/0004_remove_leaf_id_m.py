# Generated by Django 3.2.15 on 2022-09-28 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0003_alter_leaf_id_m'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leaf',
            name='id_m',
        ),
    ]