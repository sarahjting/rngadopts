# Generated by Django 4.1.4 on 2022-12-27 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('colors', '0003_alter_colorpool_adopt'),
        ('adopts', '0003_rename_count_adopt_genes_count_adopt_layers_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adoptlayer',
            name='color_pool',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='colors.colorpool'),
        ),
    ]
