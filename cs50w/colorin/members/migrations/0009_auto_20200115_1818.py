# Generated by Django 3.0.1 on 2020-01-15 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_auto_20200114_1145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='history',
            name='person',
        ),
        migrations.DeleteModel(
            name='StaffHistory',
        ),
        migrations.AddField(
            model_name='platform',
            name='type',
            field=models.IntegerField(choices=[(1, 'Social'), (2, 'Resource')], default=2),
        ),
        migrations.AddField(
            model_name='suggestion',
            name='domain',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, related_name='platform_suggestions', to='members.Platform'),
        ),
        migrations.DeleteModel(
            name='History',
        ),
    ]
