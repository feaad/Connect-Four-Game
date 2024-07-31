# Generated by Django 5.0.7 on 2024-07-29 14:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_alter_move_game'),
    ]

    operations = [
        migrations.AlterField(
            model_name='move',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.player'),
        ),
    ]