# Generated by Django 3.0.2 on 2020-05-28 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_auto_20200528_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recessedconvector',
            name='max_length',
            field=models.IntegerField(default=None, verbose_name='Максимальная длинна, мм'),
        ),
    ]