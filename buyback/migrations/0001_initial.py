# Generated by Django 3.2.19 on 2023-08-03 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EveItemTax',
            fields=[
                ('taxid', models.AutoField(primary_key=True, serialize=False)),
                ('type_id', models.IntegerField(default=0)),
                ('group_id', models.IntegerField(default=0)),
                ('type_name', models.CharField(default='', max_length=255)),
                ('amarr_buy_percentage', models.FloatField(default=0.0)),
                ('jita_buy_percentage', models.FloatField(default=0.0)),
                ('flat_cost', models.BooleanField(default=False)),
                ('hauling_fee', models.BooleanField(default=False)),
                ('jita_sell_percentage', models.FloatField(default=0.0)),
                ('effective_rate', models.FloatField(default=0.0)),
            ],
        ),
    ]
