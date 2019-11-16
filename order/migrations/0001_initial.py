# Generated by Django 2.2.1 on 2019-05-15 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0003_auto_20190514_1142'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArrivalCoord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='DepartureCoord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrival', models.CharField(max_length=257)),
                ('departure', models.CharField(max_length=257)),
                ('status', models.CharField(choices=[('search', 'Searching'), ('active', 'Active'), ('close', 'Closed')], max_length=10)),
                ('price', models.IntegerField()),
                ('arrival_coords', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='order.ArrivalCoord')),
                ('departure_coords', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='order.DepartureCoord')),
                ('passenger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Passenger')),
                ('taxi', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.Taxi')),
            ],
        ),
    ]