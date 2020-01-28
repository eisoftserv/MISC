# Generated by Django 3.0.1 on 2020-01-10 22:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_auto_20200110_2303'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='social1',
            new_name='social',
        ),
        migrations.RemoveField(
            model_name='member',
            name='social2',
        ),
        migrations.AddField(
            model_name='theme',
            name='status',
            field=models.IntegerField(choices=[(0, 'Private'), (1, 'Public'), (2, 'Archived')], default=0),
        ),
        migrations.AlterField(
            model_name='member',
            name='status',
            field=models.IntegerField(choices=[(1, 'Private'), (2, 'Public'), (3, 'Archived')], default=1),
        ),
        migrations.AlterField(
            model_name='suggestion',
            name='stamp',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='theme',
            name='stamp',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=240)),
                ('stamp', models.CharField(default='', max_length=30)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='member_sent', to='members.Member')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='member_received', to='members.Member')),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(default='', max_length=30)),
                ('stamp', models.CharField(default='', max_length=30)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='member_actions', to='members.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=240)),
                ('stamp', models.CharField(default='', max_length=30)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='member_comments', to='members.Member')),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='suggestion_comments', to='members.Suggestion')),
            ],
        ),
    ]
