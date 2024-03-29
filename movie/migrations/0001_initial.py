# Generated by Django 4.1.5 on 2023-03-14 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(help_text='Should auto fill as you add title text', max_length=200, unique=True)),
                ('genres', models.CharField(help_text='Add more than one separate using |', max_length=200)),
                ('year', models.DateField()),
                ('actors', models.CharField(help_text='Add more than one separate using |', max_length=250)),
                ('director', models.CharField(max_length=250)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-updated',),
            },
        ),
    ]
