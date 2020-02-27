# Generated by Django 3.0.3 on 2020-02-27 20:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.TextField(blank=True, max_length=100)),
                ('league', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='league.League')),
            ],
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.TextField(blank=True, max_length=10)),
                ('season', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='league.Season')),
            ],
        ),
        migrations.CreateModel(
            name='LeagueMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league.League')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='league',
            name='members',
            field=models.ManyToManyField(through='league.LeagueMembership', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.TextField(blank=True, max_length=50)),
                ('winner', models.TextField(blank=True, max_length=50)),
                ('loser', models.TextField(blank=True, max_length=50)),
                ('week', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='league.Week')),
            ],
        ),
    ]