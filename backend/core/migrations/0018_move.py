# Generated by Django 5.0.7 on 2024-07-28 08:32

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_alter_guest_username_alter_user_username_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Move',
            fields=[
                ('move_id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('column', models.IntegerField()),
                ('row', models.IntegerField()),
                ('is_undone', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('game', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.game')),
                ('player', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='core.player')),
            ],
            options={
                'verbose_name': 'Move',
                'verbose_name_plural': 'Moves',
                'ordering': ['move_id'],
            },
        ),
    ]
