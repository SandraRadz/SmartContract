# Generated by Django 3.1.6 on 2021-03-24 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_escrow_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='private_hash',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]