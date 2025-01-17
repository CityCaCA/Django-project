# Generated by Django 5.1.4 on 2025-01-06 05:06

import django.db.models.deletion
import library_api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100, unique=True, validators=[library_api.models.validate_title_is_unique])),
                ('isbn', models.CharField(max_length=100, null=True, validators=[library_api.models.validate_isbn_is_unique, library_api.models.validate_isbn])),
                ('isbn13', models.CharField(max_length=100, null=True)),
                ('author', models.CharField(max_length=100)),
                ('is_reserved', models.BooleanField(default=False)),
                ('pub_year', models.DateField(null=True)),
                ('image_url', models.CharField(max_length=200, null=True)),
                ('lang_code', models.CharField(max_length=20, null=True)),
            ],
            options={
                'verbose_name_plural': 'Books',
                'indexes': [models.Index(fields=['title'], name='title_idx')],
            },
        ),
        migrations.CreateModel(
            name='BookRatings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('num_of_1_ratings', models.IntegerField(default=0)),
                ('num_of_2_ratings', models.IntegerField(default=0)),
                ('num_of_3_ratings', models.IntegerField(default=0)),
                ('num_of_4_ratings', models.IntegerField(default=0)),
                ('num_of_5_ratings', models.IntegerField(default=0)),
                ('average_rating', models.FloatField(default=0.0)),
                ('total_num_of_ratings', models.IntegerField(default=0)),
                ('book_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='library_api.books')),
            ],
            options={
                'verbose_name_plural': 'BookRatings',
            },
        ),
    ]
