# Generated by Django 4.1.4 on 2022-12-26 13:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Adopt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('short_name', models.CharField(max_length=20, unique=True)),
                ('count', models.IntegerField(default=0)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('date_deleted', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AdoptMod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_promoted', models.DateTimeField(auto_now_add=True)),
                ('adopt', models.ForeignKey(db_column='adopt_id', on_delete=django.db.models.deletion.RESTRICT, to='adopts.adopt')),
                ('mod', models.ForeignKey(db_column='mod_id', on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AdoptLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discord_user_id', models.IntegerField(db_index=True, null=True)),
                ('discord_guild_id', models.IntegerField(db_index=True, null=True)),
                ('discord_channel_id', models.IntegerField(db_index=True, null=True)),
                ('discord_message_id', models.IntegerField(db_index=True, null=True)),
                ('image_url', models.CharField(max_length=120)),
                ('command', models.TextField()),
                ('result', models.JSONField()),
                ('adopt', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='adopts.adopt')),
                ('mod', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='adopt',
            name='mods',
            field=models.ManyToManyField(through='adopts.AdoptMod', to=settings.AUTH_USER_MODEL),
        ),
    ]
