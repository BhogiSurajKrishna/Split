# Generated by Django 2.2.6 on 2019-11-23 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_auto_20191123_1014'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='status',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]