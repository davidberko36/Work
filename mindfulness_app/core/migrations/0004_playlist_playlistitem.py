# Generated by Django 5.1.1 on 2024-09-11 15:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_audiotrack_scheduledsession'),
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlayListItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AudioTrack', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.audiotrack')),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.playlist')),
            ],
        ),
    ]
