# Generated by Django 2.2.6 on 2019-11-24 14:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0027_auto_20191124_0602'),
    ]

    operations = [
        migrations.AddField(
            model_name='add_group',
            name='group_pk',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.CreateModel(
            name='pair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(blank=True, default=0)),
                ('current_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='in_groups', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='add_group',
            name='users',
            field=models.ManyToManyField(to='accounts.pair'),
        ),
    ]