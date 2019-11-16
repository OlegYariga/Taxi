# Generated by Django 2.2.1 on 2019-05-14 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190513_1631'),
    ]

    operations = [
        migrations.CreateModel(
            name='Taxi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('econom', 'Econom class'), ('business', 'Business class'), ('first', 'First class'), ('keke', 'Tricycle(Keke)')], default='econom', max_length=15)),
                ('price', models.IntegerField(default=10)),
            ],
        ),
        migrations.AddField(
            model_name='driver',
            name='taxi',
            field=models.OneToOneField(default=3, on_delete=django.db.models.deletion.CASCADE, to='users.Taxi'),
            preserve_default=False,
        ),
    ]
