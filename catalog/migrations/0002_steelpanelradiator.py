# Generated by Django 3.0.2 on 2020-05-08 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SteelPanelRadiator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=400, verbose_name='Модель')),
                ('height', models.IntegerField(verbose_name='Высота')),
                ('width', models.IntegerField(verbose_name='Ширина')),
                ('depth', models.IntegerField(verbose_name='Глубина')),
                ('center_distance', models.IntegerField(verbose_name='Межосевое расстояние')),
                ('photo', models.ImageField(blank=True, default=None, upload_to='steel_panel_images', verbose_name='Картинка')),
                ('description', models.TextField(verbose_name='Описание')),
                ('power', models.CharField(max_length=120, verbose_name='Мощность (50 / 60 / 70)')),
                ('pressure', models.IntegerField(verbose_name='Рабочее давление')),
                ('weight', models.FloatField(verbose_name='Вес')),
                ('price', models.FloatField(default=0, verbose_name='Цена')),
                ('connection_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.ConnectionType', verbose_name='Тип подключения')),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Manufacturer', verbose_name='Производитель')),
            ],
            options={
                'verbose_name': 'Стальной панельный радиатор',
                'verbose_name_plural': 'Стальные панельные радиаторы',
                'db_table': 'Steel Panel Radiator',
            },
        ),
    ]
