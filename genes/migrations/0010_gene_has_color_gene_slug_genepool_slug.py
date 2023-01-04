# Generated by Django 4.1.4 on 2023-01-03 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genes', '0009_rename_required_gene_id_genelayer_required_gene'),
    ]

    operations = [
        migrations.AddField(
            model_name='gene',
            name='has_color',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='gene',
            name='slug',
            field=models.CharField(default='', max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='genepool',
            name='slug',
            field=models.CharField(default='', max_length=40),
            preserve_default=False,
        ),
        migrations.RunSQL("""
            UPDATE genes_gene SET slug = regexp_replace(lower(trim(name)), '[^a-z0-9\\-_]+', '', 'gi')
        """),
        migrations.RunSQL("""
            UPDATE genes_genepool SET slug = regexp_replace(lower(trim(name)), '[^a-z0-9\\-_]+', '', 'gi')
        """),
    ]