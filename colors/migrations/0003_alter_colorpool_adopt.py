# Generated by Django 4.1.4 on 2022-12-27 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adopts', '0003_rename_count_adopt_genes_count_adopt_layers_count_and_more'),
        ('colors', '0002_alter_colorpool_adopt_alter_colorpool_colors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colorpool',
            name='adopt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='color_pools', to='adopts.adopt'),
        ),
    ]
