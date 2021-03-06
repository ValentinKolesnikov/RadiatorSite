# Generated by Django 3.0.2 on 2020-05-12 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_costironmanufacturer_costironradiator'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConvectorType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Название')),
                ('photo', models.ImageField(blank=True, default=None, upload_to='component_types_images', verbose_name='Картинка')),
            ],
            options={
                'verbose_name': 'Тип конвектора',
                'verbose_name_plural': 'Типы конвекторов',
                'db_table': 'Convector Type',
            },
        ),
    ]
