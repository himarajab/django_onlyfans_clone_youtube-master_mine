# Generated by Django 3.1.5 on 2021-02-13 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tier', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='tier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tier', to='tier.tier'),
        ),
    ]
