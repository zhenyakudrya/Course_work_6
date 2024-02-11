# Generated by Django 5.0.1 on 2024-02-10 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Заголовок')),
                ('content', models.TextField(verbose_name='текст')),
                ('preview', models.ImageField(blank=True, null=True, upload_to='blog/', verbose_name='изображение')),
                ('views_count', models.IntegerField(default=0, verbose_name='количество просмотров')),
                ('public_date', models.DateField(auto_now=True)),
            ],
        ),
    ]