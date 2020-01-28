# Generated by Django 3.0.1 on 2020-01-27 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0015_auto_20200124_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='name',
            field=models.CharField(db_index=True, max_length=80),
        ),
        migrations.AlterField(
            model_name='suggestion',
            name='author',
            field=models.CharField(blank=True, default='', max_length=160),
        ),
    ]
