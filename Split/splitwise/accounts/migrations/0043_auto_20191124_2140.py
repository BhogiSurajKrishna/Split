# Generated by Django 2.2.6 on 2019-11-24 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0042_auto_20191124_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='add_group',
            name='users',
            field=models.ManyToManyField(to='accounts.Pair'),
        ),
        migrations.AlterField(
            model_name='group_transactions',
            name='group',
            field=models.ManyToManyField(to='accounts.Add_group'),
        ),
    ]