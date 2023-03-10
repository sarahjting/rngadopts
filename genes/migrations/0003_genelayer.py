# Generated by Django 4.1.4 on 2022-12-27 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adopts', '0003_rename_count_adopt_genes_count_adopt_layers_count_and_more'),
        ('genes', '0002_genepool_sort_alter_gene_gene_pool_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneLayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='')),
                ('type', models.CharField(choices=[('static_over', 'Static image on top of adopt (eg. tert lines)'), ('shading', 'Shading (eg. tert shading -- dropshadows also work)'), ('highlights', 'Highlights (eg. tert highlights)'), ('static_marking', 'Static image on adopt base (eg. accent/tattoo)'), ('color', 'Generate all colors from color pool (regular marking)'), ('static_under', 'Static image underneath adopt (eg. background)')], max_length=20)),
                ('color_key', models.IntegerField(null=True)),
                ('sort', models.IntegerField(default=0)),
                ('gene', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='gene_layers', to='adopts.adopt')),
            ],
        ),
    ]
