# Generated by Django 3.0.2 on 2020-05-08 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Название')),
                ('code', models.CharField(max_length=6, verbose_name='Код цвета (HEX)')),
            ],
            options={
                'verbose_name': 'Цвет',
                'verbose_name_plural': 'Цвета',
                'db_table': 'Color',
            },
        ),
        migrations.CreateModel(
            name='ComponentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Название')),
                ('photo', models.ImageField(blank=True, default=None, upload_to='component_types_images', verbose_name='Картинка')),
            ],
            options={
                'verbose_name': 'Тип комплектующих',
                'verbose_name_plural': 'Типы комплектующих',
                'db_table': 'Component Type',
            },
        ),
        migrations.CreateModel(
            name='ConnectionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Тип подключения',
                'verbose_name_plural': 'Типы подключения',
                'db_table': 'Connection Type',
            },
        ),
        migrations.CreateModel(
            name='DesignManufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Название')),
                ('country', models.CharField(max_length=120, verbose_name='Страна')),
                ('description', models.CharField(max_length=300, verbose_name='Описание')),
                ('photo', models.ImageField(blank=True, default=None, upload_to='design_manufacturers_images', verbose_name='Картинка')),
            ],
            options={
                'verbose_name': 'Производитель дизайн-радиаторов',
                'verbose_name_plural': 'Производители дизайн-радиаторов',
                'db_table': 'Design Manufacturer',
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Название')),
                ('country', models.CharField(max_length=120, verbose_name='Страна')),
            ],
            options={
                'verbose_name': 'Производитель',
                'verbose_name_plural': 'Производители',
                'db_table': 'Manufacturer',
            },
        ),
        migrations.CreateModel(
            name='DesignRadiator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=400, verbose_name='Модель')),
                ('height', models.IntegerField(verbose_name='Высота')),
                ('width', models.IntegerField(verbose_name='Ширина')),
                ('photo', models.ImageField(blank=True, default=None, upload_to='design_images', verbose_name='Картинка')),
                ('description', models.TextField(verbose_name='Описание')),
                ('power', models.CharField(max_length=120, verbose_name='Мощность (50 / 60 / 70)')),
                ('pressure', models.IntegerField(verbose_name='Рабочее давление')),
                ('weight', models.FloatField(verbose_name='Вес')),
                ('price', models.FloatField(default=0, verbose_name='Цена')),
                ('colors', models.ManyToManyField(default=None, to='catalog.Color', verbose_name='Цвета')),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.DesignManufacturer', verbose_name='Производитель')),
            ],
            options={
                'verbose_name': 'Дизайн радиатор',
                'verbose_name_plural': 'Дизайн радиаторы',
                'db_table': 'Design Radiator',
            },
        ),
        migrations.CreateModel(
            name='ComponentPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название')),
                ('photo', models.ImageField(blank=True, default=None, upload_to='aluminium_images', verbose_name='Картинка')),
                ('description', models.TextField(verbose_name='Описание')),
                ('price', models.FloatField(default=0, verbose_name='Цена')),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Manufacturer', verbose_name='Производитель')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.ComponentType', verbose_name='Тип')),
            ],
            options={
                'verbose_name': 'Комплектующее',
                'verbose_name_plural': 'Комплектующие',
                'db_table': 'Component Part',
            },
        ),
        migrations.CreateModel(
            name='BimetalRadiator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=400, verbose_name='Модель')),
                ('height', models.IntegerField(verbose_name='Высота')),
                ('width', models.IntegerField(verbose_name='Ширина')),
                ('depth', models.IntegerField(verbose_name='Глубина')),
                ('center_distance', models.IntegerField(verbose_name='Межосевое расстояние')),
                ('photo', models.ImageField(blank=True, default=None, upload_to='bimetal_images', verbose_name='Картинка')),
                ('description', models.TextField(verbose_name='Описание')),
                ('power', models.CharField(max_length=120, verbose_name='Мощность (50 / 60 / 70)')),
                ('pressure', models.IntegerField(verbose_name='Рабочее давление')),
                ('weight', models.FloatField(verbose_name='Вес')),
                ('price', models.FloatField(default=0, verbose_name='Цена')),
                ('colors', models.ManyToManyField(default=None, to='catalog.Color', verbose_name='Цвета')),
                ('connection_type', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='catalog.ConnectionType', verbose_name='Тип подключения')),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Manufacturer', verbose_name='Производитель')),
            ],
            options={
                'verbose_name': 'Биметаллический радиатор',
                'verbose_name_plural': 'Биметаллические радиаторы',
                'db_table': 'Bimetal Radiator',
            },
        ),
        migrations.CreateModel(
            name='AluminiumRadiator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=400, verbose_name='Модель')),
                ('height', models.IntegerField(verbose_name='Высота')),
                ('width', models.IntegerField(verbose_name='Ширина')),
                ('depth', models.IntegerField(verbose_name='Глубина')),
                ('center_distance', models.IntegerField(verbose_name='Межосевое расстояние')),
                ('photo', models.ImageField(blank=True, default=None, upload_to='aluminium_images', verbose_name='Картинка')),
                ('description', models.TextField(verbose_name='Описание')),
                ('power', models.CharField(max_length=120, verbose_name='Мощность (50 / 60 / 70)')),
                ('pressure', models.IntegerField(verbose_name='Рабочее давление')),
                ('weight', models.FloatField(verbose_name='Вес')),
                ('price', models.FloatField(default=0, verbose_name='Цена')),
                ('connection_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.ConnectionType', verbose_name='Тип подключения')),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Manufacturer', verbose_name='Производитель')),
            ],
            options={
                'verbose_name': 'Алюминиевый радиатор',
                'verbose_name_plural': 'Алюминиевые радиаторы',
                'db_table': 'Aluminium Radiator',
            },
        ),
    ]
