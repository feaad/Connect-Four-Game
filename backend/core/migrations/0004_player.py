# Generated by Django 5.0.7 on 2024-07-22 07:27

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_algorithm'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('player_id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_human', models.BooleanField(default=True)),
                ('wins', models.IntegerField(default=0)),
                ('losses', models.IntegerField(default=0)),
                ('draws', models.IntegerField(default=0)),
                ('total_games', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('algorithm', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='core.algorithm')),
                ('guest', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='core.guest')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
