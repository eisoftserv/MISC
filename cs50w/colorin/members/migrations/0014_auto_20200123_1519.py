# Generated by Django 3.0.1 on 2020-01-23 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0013_auto_20200122_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flag',
            name='itemtype',
            field=models.IntegerField(choices=[(1, 'Suggestion'), (2, 'Comment'), (3, 'Message'), (4, 'Profile')], default=1),
        ),
    ]
