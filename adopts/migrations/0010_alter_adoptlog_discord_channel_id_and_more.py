# Generated by Django 4.1.4 on 2023-01-01 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adopts', '0009_adopt_current_display_id_adopt_gen_caption_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adoptlog',
            name='discord_channel_id',
            field=models.CharField(db_index=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='adoptlog',
            name='discord_guild_id',
            field=models.CharField(db_index=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='adoptlog',
            name='discord_message_id',
            field=models.CharField(db_index=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='adoptlog',
            name='discord_user_id',
            field=models.CharField(db_index=True, max_length=64, null=True),
        ),
    ]
