# Generated by Django 4.1.4 on 2022-12-30 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adopts', '0007_remove_adoptlayer_color_pool_adoptlayer_gene_pool_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='adoptlayer',
            options={'ordering': ('-sort',)},
        ),
        migrations.AddField(
            model_name='adopt',
            name='height',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='adopt',
            name='width',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
    ]
