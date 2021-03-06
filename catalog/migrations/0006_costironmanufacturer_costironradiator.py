# Generated by Django 3.0.2 on 2020-05-11 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_auto_20200509_1504'),
    ]

    operations = [
        migrations.CreateModel(
            name='CostIronManufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Название')),
                ('country', models.CharField(max_length=120, verbose_name='Страна')),
                ('description', models.CharField(max_length=300, verbose_name='Описание')),
                ('photo', models.ImageField(blank=True, default=None, upload_to='cost_iron_manufacturers_images', verbose_name='Картинка')),
            ],
            options={
                'verbose_name': 'Производитель чугунных радиаторов',
                'verbose_name_plural': 'Производители чугунных радиаторов',
                'db_table': 'Cost Iron Manufacturer',
            },
        ),
        migrations.CreateModel(
            name='CostIronRadiator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=400, verbose_name='Модель')),
                ('height', models.IntegerField(verbose_name='Высота')),
                ('width', models.IntegerField(verbose_name='Ширина')),
                ('depth', models.IntegerField(verbose_name='Глубина')),
                ('center_distance', models.IntegerField(verbose_name='Межосевое расстояние')),
                ('photo', models.ImageField(blank=True, default=None, upload_to='cost_iron_images', verbose_name='Картинка')),
                ('description', models.TextField(verbose_name='Описание')),
                ('power', models.CharField(max_length=120, verbose_name='Мощность (50 / 60 / 70)')),
                ('pressure', models.IntegerField(verbose_name='Рабочее давление')),
                ('weight', models.FloatField(verbose_name='Вес')),
                ('price', models.FloatField(default=0, verbose_name='Цена')),
                ('connection_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.ConnectionType', verbose_name='Тип подключения')),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.CostIronManufacturer', verbose_name='Производитель')),
            ],
            options={
                'verbose_name': 'Чугунный радиатор',
                'verbose_name_plural': 'Чугунные радиаторы',
                'db_table': 'Cost Iron Radiator',
            },
        ),
    ]
