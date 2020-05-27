# Generated by Django 3.0.2 on 2020-05-20 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_delete_convectortype'),
    ]

    operations = [
        migrations.CreateModel(
            name='WallConvector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=400, verbose_name='Модель')),
                ('height', models.IntegerField(verbose_name='Высота')),
                ('width', models.IntegerField(verbose_name='Ширина')),
                ('length', models.IntegerField(verbose_name='Длина')),
                ('photo', models.ImageField(blank=True, default=None, upload_to='wall_convector_images', verbose_name='Картинка')),
                ('description', models.TextField(verbose_name='Описание')),
                ('temperature', models.FloatField(verbose_name='Максимальная рабочая температура')),
                ('pressure', models.FloatField(verbose_name='Максимальное рабочее давление')),
                ('heat_output', models.FloatField(verbose_name='Выход тепла')),
                ('surface_temperature', models.FloatField(verbose_name='Максимальная температура поверхности')),
                ('connection', models.CharField(max_length=200, verbose_name='Подключение')),
                ('price', models.FloatField(default=0, verbose_name='Цена')),
                ('connection_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.ConnectionType', verbose_name='Тип подключения')),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Manufacturer', verbose_name='Производитель')),
            ],
            options={
                'verbose_name': 'Настенный конвектор',
                'verbose_name_plural': 'Настенные конвекторы',
                'db_table': 'Wall Convector',
            },
        ),
    ]