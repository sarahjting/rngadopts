# Generated by Django 4.1.4 on 2022-12-26 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('adopts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ColorPool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('date_deleted', models.DateTimeField(null=True)),
                ('colors', models.JSONField()),
                ('adopt', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='adopts.adopt')),
            ],
        ),
    ]