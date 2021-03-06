# Generated by Django 2.2.6 on 2019-11-23 10:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0020_auto_20191114_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='debt',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(blank=True, default=0)),
                ('payable', models.IntegerField(blank=True, default=0)),
                ('type', models.CharField(choices=[('a', 'paid by you and split equally'), ('b', 'paid by your friend and split equally'), ('c', 'You owe to him completely'), ('d', 'He owe to you completely'), ('e', (('1', 'paid by you and split by shares'), ('2', 'paid by friend and split by shares'), ('3', 'paid by you and split by percentages'), ('4', 'paid by friend and split by percentages')))], default='green', max_length=5)),
                ('desc', models.CharField(max_length=100)),
                ('tag', models.CharField(max_length=100)),
                ('current_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owners', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
