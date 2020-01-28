# Generated by Django 3.0.1 on 2020-01-11 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_auto_20200111_1630'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='blockedsender',
            name='members_blo_sender__8f971b_idx',
        ),
        migrations.RemoveIndex(
            model_name='blockedsender',
            name='members_blo_recipie_f25639_idx',
        ),
        migrations.RemoveIndex(
            model_name='staffhistory',
            name='members_sta_staff_3940c8_idx',
        ),
        migrations.AlterField(
            model_name='member',
            name='djemail',
            field=models.EmailField(db_index=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='member',
            name='djuser',
            field=models.CharField(db_index=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='member',
            name='name',
            field=models.CharField(db_index=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='staffhistory',
            name='staff',
            field=models.CharField(db_index=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='theme',
            name='name',
            field=models.CharField(db_index=True, max_length=80),
        ),
    ]