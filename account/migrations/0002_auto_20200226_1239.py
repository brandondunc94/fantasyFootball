# Generated by Django 3.0.3 on 2020-02-26 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0001_initial'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='birth_date',
        ),
        migrations.AddField(
            model_name='profile',
            name='league',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='league.League'),
        ),
    ]
