# Generated by Django 4.2.3 on 2023-09-20 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MH_App', '0011_alter_order_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.TextField(max_length=200),
        ),
        migrations.AlterField(
            model_name='order',
            name='city',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='order',
            name='country',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='order',
            name='lastname',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='order',
            name='state',
            field=models.CharField(max_length=200),
        ),
    ]
