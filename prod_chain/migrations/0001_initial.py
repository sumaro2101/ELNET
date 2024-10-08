# Generated by Django 5.0.7 on 2024-09-11 16:49

import django.db.models.deletion
import django_countries.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Имя сети или завода', max_length=250, verbose_name='имя')),
                ('role', models.CharField(choices=[('factory', 'Завод'), ('retail', 'Розничная сеть'), ('entrepreneur', 'Предприниматель')], help_text='Какую роль исполняет объект', max_length=50, verbose_name='Тип роли')),
                ('email', models.EmailField(help_text='Email контакта', max_length=254, verbose_name='Email')),
                ('country', django_countries.fields.CountryField(db_index=True, help_text='Страна контакта', max_length=2, verbose_name='страна')),
                ('town', models.CharField(help_text='Город контакта', max_length=254, verbose_name='город')),
                ('street', models.CharField(help_text='Улица контакта', max_length=254, verbose_name='улица')),
                ('build', models.CharField(help_text='Номер дома контакта', max_length=10, verbose_name='дом')),
            ],
            options={
                'verbose_name': 'контакт',
                'verbose_name_plural': 'контакты',
            },
        ),
        migrations.CreateModel(
            name='ProdMap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duty', models.DecimalField(decimal_places=2, help_text='Долг перед поставщиком', max_digits=13, verbose_name='долг')),
                ('appoiment_date', models.DateTimeField(auto_now_add=True, help_text='Дата назначения', verbose_name='дата')),
            ],
            options={
                'verbose_name': 'сеть',
                'verbose_name_plural': 'сети',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='название продукта', max_length=254, verbose_name='название')),
                ('model', models.CharField(help_text='модель продукта', max_length=254, verbose_name='модель')),
                ('realize', models.DateField(help_text='Дата выхода продукта на рынок', verbose_name='дата выхода')),
            ],
            options={
                'verbose_name': 'продукт',
                'verbose_name_plural': 'продукты',
            },
        ),
        migrations.AddConstraint(
            model_name='contact',
            constraint=models.UniqueConstraint(fields=('name', 'role', 'country'), name='unique_contact'),
        ),
        migrations.AddField(
            model_name='prodmap',
            name='prod_object',
            field=models.ForeignKey(help_text='Целевой объект цепочки', on_delete=django.db.models.deletion.PROTECT, to='prod_chain.contact', verbose_name='объект'),
        ),
        migrations.AddField(
            model_name='prodmap',
            name='supplier',
            field=models.ForeignKey(help_text='Поставщик', null=True, on_delete=django.db.models.deletion.CASCADE, to='prod_chain.prodmap', verbose_name='поставщик'),
        ),
        migrations.AddField(
            model_name='prodmap',
            name='products',
            field=models.ManyToManyField(help_text='Товары объекта', to='prod_chain.product', verbose_name='товары'),
        ),
    ]
