# Generated by Django 3.2.15 on 2022-09-28 19:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Leaf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_m', models.PositiveIntegerField(auto_created=True, null=True, verbose_name='Уникальный ID')),
                ('main_menu', models.BooleanField(default=False, verbose_name='Главное меню')),
                ('leaf', models.CharField(max_length=64, verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.PositiveIntegerField(unique=True, verbose_name='ID пользователя')),
                ('user_name', models.TextField(blank=True, default='username', null=True, verbose_name='Username')),
                ('first_name', models.TextField(default='name', verbose_name='Имя')),
                ('last_message', models.TextField(default='', verbose_name='Последнее сообщение')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='Tree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='treeBranch', to='ugc.leaf', verbose_name='Ветка')),
                ('leaf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='treeLeaf', to='ugc.leaf', verbose_name='Листок')),
            ],
            options={
                'verbose_name': 'Ветка',
                'verbose_name_plural': 'Ветки',
            },
        ),
        migrations.CreateModel(
            name='Bearing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='Название/Заголовок')),
                ('description', models.TextField(verbose_name='Описание')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='Цена')),
                ('tree', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ugc.tree', verbose_name='Каталог')),
            ],
            options={
                'verbose_name': 'Подшибник',
                'verbose_name_plural': 'Подшибники',
            },
        ),
    ]
