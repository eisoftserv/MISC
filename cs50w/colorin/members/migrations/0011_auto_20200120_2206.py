# Generated by Django 3.0.1 on 2020-01-20 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0010_auto_20200119_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flag',
            name='itemtype',
            field=models.IntegerField(choices=[(1, 'Suggestion'), (2, 'Comment'), (3, 'Message'), (4, 'Member')], default=1),
        ),
    ]
