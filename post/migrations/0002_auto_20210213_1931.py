# Generated by Django 3.1.5 on 2021-02-13 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stream',
            name='visible',
            field=models.BooleanField(default=False),
        ),
    ]
