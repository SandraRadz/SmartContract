# Generated by Django 3.1.6 on 2021-03-24 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0004_product_contract_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='currency',
            field=models.CharField(default='wei', max_length=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('new', 'NEW'), ('pending_order', 'PENDING ORDER'), ('order', 'ORDER'), ('pending_send', 'PENDING SEND'), ('sent', 'SENT'), ('pending_received', 'PENDING RECEIVED'), ('received', 'RECEIVED'), ('problem', 'PROBLEM')], default='new', max_length=20),
        ),
    ]
