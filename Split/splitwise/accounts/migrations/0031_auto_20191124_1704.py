# Generated by Django 2.2.6 on 2019-11-24 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0030_auto_20191124_1612'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group_Transactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='add_group',
            name='users',
            field=models.ManyToManyField(to='accounts.Pair'),
        ),
        migrations.DeleteModel(
            name='group_member',
        ),
        migrations.AddField(
            model_name='group_transactions',
            name='group',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.Add_group'),
        ),
    ]
