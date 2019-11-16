# Generated by Django 2.2.1 on 2019-05-16 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_order_payment_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_type',
            field=models.CharField(choices=[('card', 'card'), ('cash', 'cash')], max_length=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('search', 'searching'), ('active', 'active'), ('close', 'closed')], default='search', max_length=10),
        ),
    ]
