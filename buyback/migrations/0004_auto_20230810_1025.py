# Generated by Django 3.2.19 on 2023-08-10 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyback', '0003_eveitemtax_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='eveitemtax',
            name='category_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='eveitemtax',
            name='category_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
