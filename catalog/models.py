from django.db import models
from django.utils.safestring import mark_safe
from .choices import *


class SideType(models.Model):
    class Meta:
        db_table = "Side Type"
        verbose_name = "Тип бортика"
        verbose_name_plural = "Типы бортика"

    name = models.CharField("Название", max_length=500)

    def __str__(self):
        return self.name


class LatticeType(models.Model):
    class Meta:
        db_table = "Lattice Type"
        verbose_name = "Тип решетки"
        verbose_name_plural = "Типы решеток"

    name = models.CharField("Название", max_length=500)

    def __str__(self):
        return self.name


class RecessedConvectorModel(models.Model):
    class Meta:
        db_table = "Recessed Convector Model"
        verbose_name = "Модель встаиваемого конвектора"
        verbose_name_plural = "Модели встаиваемых конвекторов"

    name = models.CharField("Название", max_length=300)

    def __str__(self):
        return self.name


class ApplianceType(models.Model):
    class Meta:
        db_table = "ApplianceType"
        verbose_name = "Тип прибора"
        verbose_name_plural = "Типы прибора"

    name = models.CharField("Название", max_length=120)

    def __str__(self):
        return self.name


class Color(models.Model):
    class Meta:
        db_table = "Color"
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"

    name = models.CharField("Название", max_length=120)
    code = models.CharField("Код цвета (HEX)", max_length=6)

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    class Meta:
        db_table = "Manufacturer"
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"

    name = models.CharField("Название", max_length=120)
    country = models.CharField("Страна", max_length=120)

    def __str__(self):
        return self.name


class ManufacturerDescription(models.Model):
    class Meta:
        db_table = "Manufacturer Description"
        verbose_name = "Описание производителя"
        verbose_name_plural = "Описания производителей"

    manufacturer = models.ForeignKey(Manufacturer, verbose_name="Производитель", on_delete=models.CASCADE)
    radiator_type = models.IntegerField("Тип радиоторов", choices=RADIATOR_TYPE_CHOICES, default=1)
    description = models.CharField("Описание", max_length=300)
    photo = models.ImageField("Картинка", blank=True, upload_to="manufacturers_description_images", default=None)

    def __str__(self):
        return self.description

    def show_image(self):
        if self.photo:
            return mark_safe(
                u'<a href="{0}" target="_blank"><img style="object-fit: contain;" src="{0}" width="100" height="150"/></a>'.format(
                    self.photo.url))
        else:
            return '(Нет изображения)'

    show_image.short_description = 'Изображение'
    show_image.allow_tags = True


class ComponentType(models.Model):
    class Meta:
        db_table = "Component Type"
        verbose_name = "Тип комплектующих"
        verbose_name_plural = "Типы комплектующих"

    name = models.CharField("Название", max_length=120)
    photo = models.ImageField("Картинка", blank=True, upload_to="component_types_images", default=None)

    def __str__(self):
        return self.name


class ConnectionType(models.Model):
    class Meta:
        db_table = "Connection Type"
        verbose_name = "Тип подключения"
        verbose_name_plural = "Типы подключения"

    name = models.CharField("Название", max_length=200)

    def __str__(self):
        return f"{self.name}"


class ComponentPart(models.Model):
    class Meta:
        db_table = "Component Part"
        verbose_name = "Комплектующее"
        verbose_name_plural = "Комплектующие"

    name = models.CharField("Название", max_length=500)
    photo = models.ImageField("Картинка", blank=True, upload_to="aluminium_images", default=None)
    description = models.TextField("Описание")
    type = models.ForeignKey(ComponentType, on_delete=models.CASCADE, verbose_name="Тип")
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель")
    price = models.FloatField("Цена", default=0)

    def __str__(self):
        return f'{self.type} {self.manufacturer} {self.name}'

    def show_image(self):
        if self.photo:
            return mark_safe(
                u'<a href="{0}" target="_blank"><img style="object-fit: contain;" src="{0}" width="100" height="150"/></a>'.format(
                    self.photo.url))
        else:
            return '(Нет изображения)'

    show_image.short_description = 'Изображение'
    show_image.allow_tags = True


class AluminiumRadiator(models.Model):
    class Meta:
        db_table = "Aluminium Radiator"
        verbose_name = "Алюминиевый радиатор"
        verbose_name_plural = "Алюминиевые радиаторы"

    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель")
    model_name = models.CharField("Модель", max_length=400)
    height = models.IntegerField("Высота")
    width = models.IntegerField("Ширина")
    depth = models.IntegerField("Глубина")
    center_distance = models.IntegerField("Межосевое расстояние")
    photo = models.ImageField("Картинка", blank=True, upload_to="aluminium_images", default=None)
    description = models.TextField("Описание")
    power = models.CharField("Мощность (50 / 60 / 70)", max_length=120)
    pressure = models.IntegerField("Рабочее давление")
    weight = models.FloatField("Вес")
    price = models.FloatField("Цена", default=0)
    connection_type = models.ForeignKey(ConnectionType, on_delete=models.CASCADE, verbose_name="Тип подключения")

    def __str__(self):
        return self.model_name

    def show_image(self):
        if self.photo:
            return mark_safe(
                u'<a href="{0}" target="_blank"><img style="object-fit: contain;" src="{0}" width="100" height="150"/></a>'.format(
                    self.photo.url))
        else:
            return '(Нет изображения)'

    show_image.short_description = 'Изображение'
    show_image.allow_tags = True


class BimetalRadiator(models.Model):
    class Meta:
        db_table = "Bimetal Radiator"
        verbose_name = "Биметаллический радиатор"
        verbose_name_plural = "Биметаллические радиаторы"

    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель")
    model_name = models.CharField("Модель", max_length=400)
    height = models.IntegerField("Высота")
    width = models.IntegerField("Ширина")
    depth = models.IntegerField("Глубина")
    center_distance = models.IntegerField("Межосевое расстояние")
    connection_type = models.ForeignKey(ConnectionType, verbose_name="Тип подключения", on_delete=models.CASCADE,
                                        default=1)
    photo = models.ImageField("Картинка", blank=True, upload_to="bimetal_images", default=None)
    description = models.TextField("Описание")
    power = models.CharField("Мощность (50 / 60 / 70)", max_length=120)
    pressure = models.IntegerField("Рабочее давление")
    weight = models.FloatField("Вес")
    colors = models.ManyToManyField(Color, verbose_name="Цвета", default=None)
    price = models.FloatField("Цена", default=0)

    def __str__(self):
        return self.model_name

    def show_image(self):
        if self.photo:
            return mark_safe(
                u'<a href="{0}" target="_blank"><img style="object-fit: contain;" src="{0}" width="100" height="150"/></a>'.format(
                    self.photo.url))
        else:
            return '(Нет изображения)'

    show_image.short_description = 'Изображение'
    show_image.allow_tags = True


class DesignRadiator(models.Model):
    class Meta:
        db_table = "Design Radiator"
        verbose_name = "Дизайн радиатор"
        verbose_name_plural = "Дизайн радиаторы"

    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель", default="")
    model_name = models.CharField("Модель", max_length=400)
    height = models.IntegerField("Высота")
    width = models.IntegerField("Ширина")
    photo = models.ImageField("Картинка", blank=True, upload_to="design_images", default=None)
    description = models.TextField("Описание")
    power = models.CharField("Мощность (50 / 60 / 70)", max_length=120)
    pressure = models.IntegerField("Рабочее давление")
    weight = models.FloatField("Вес")
    colors = models.ManyToManyField(Color, verbose_name="Цвета", default=None)
    price = models.FloatField("Цена", default=0)

    def __str__(self):
        return self.model_name

    def show_image(self):
        if self.photo:
            return mark_safe(
                u'<a href="{0}" target="_blank"><img style="object-fit: contain;" src="{0}" width="100" height="150"/></a>'.format(
                    self.photo.url))
        else:
            return '(Нет изображения)'

    show_image.short_description = 'Изображение'
    show_image.allow_tags = True


class SteelPanelRadiator(models.Model):
    class Meta:
        db_table = "Steel Panel Radiator"
        verbose_name = "Стальной панельный радиатор"
        verbose_name_plural = "Стальные панельные радиаторы"

    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель")
    model_name = models.CharField("Модель", max_length=400)
    height = models.IntegerField("Высота")
    width = models.IntegerField("Ширина")
    depth = models.IntegerField("Глубина")
    center_distance = models.IntegerField("Межосевое расстояние")
    photo = models.ImageField("Картинка", blank=True, upload_to="steel_panel_images", default=None)
    description = models.TextField("Описание")
    power = models.CharField("Мощность (50 / 60 / 70)", max_length=120)
    pressure = models.IntegerField("Рабочее давление")
    weight = models.FloatField("Вес")
    price = models.FloatField("Цена", default=0)
    connection_type = models.ForeignKey(ConnectionType, on_delete=models.CASCADE, verbose_name="Тип подключения")

    def __str__(self):
        return self.model_name

    def show_image(self):
        if self.photo:
            return mark_safe(
                u'<a href="{0}" target="_blank"><img style="object-fit: contain;" src="{0}" width="100" height="150"/></a>'.format(
                    self.photo.url))
        else:
            return '(Нет изображения)'

    show_image.short_description = 'Изображение'
    show_image.allow_tags = True


class SteelTubularRadiator(models.Model):
    class Meta:
        db_table = "Steel Tubular Radiator"
        verbose_name = "Стальной трубчатый радиатор"
        verbose_name_plural = "Стальные трубчатые радиаторы"

    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель")
    model_name = models.CharField("Модель", max_length=400)
    height = models.IntegerField("Высота")
    width = models.IntegerField("Ширина")
    depth = models.IntegerField("Глубина")
    photo = models.ImageField("Картинка", blank=True, upload_to="steel_tubular_images", default=None)
    description = models.TextField("Описание")
    power = models.CharField("Мощность (50 / 60 / 70)", max_length=120)
    pressure = models.IntegerField("Рабочее давление")
    weight = models.FloatField("Вес")
    price = models.FloatField("Цена", default=0)
    connection_type = models.ForeignKey(ConnectionType, on_delete=models.CASCADE, verbose_name="Тип подключения")

    def __str__(self):
        return self.model_name

    def show_image(self):
        if self.photo:
            return mark_safe(
                u'<a href="{0}" target="_blank"><img style="object-fit: contain;" src="{0}" width="100" height="150"/></a>'.format(
                    self.photo.url))
        else:
            return '(Нет изображения)'

    show_image.short_description = 'Изображение'
    show_image.allow_tags = True


class SteelTubularKZTORadiator(models.Model):
    class Meta:
        db_table = "Steel Tubular KZTO Radiator"
        verbose_name = "Стальной трубчатый радиатор фирмы KZTO"
        verbose_name_plural = "Стальные трубчатые радиаторы фирмы KZTO"

    manufacturer_name = models.CharField(max_length=100, default='KZTO', editable=False)
    manufacturer_country = models.CharField(max_length=100, default='Россия', editable=False)
    model_name = models.CharField("Модель", max_length=400)
    appliance_type = models.ForeignKey(ApplianceType, verbose_name="Тип прибора", on_delete=models.CASCADE)
    length = models.IntegerField("Длина прибора")
    mounting_size = models.IntegerField("Монтажный размер")
    photo = models.ImageField("Картинка", blank=True, upload_to="steel_tubular_images", default=None)
    description = models.TextField("Описание")
    power = models.CharField("Мощность (70)", max_length=120)
    pressure = models.IntegerField("Рабочее давление")
    weight = models.FloatField("Вес")
    price = models.FloatField("Цена", default=0)
    connection_type = models.ForeignKey(ConnectionType, on_delete=models.CASCADE, verbose_name="Тип подключения")

    def __str__(self):
        return self.model_name

    def show_image(self):
        if self.photo:
            return mark_safe(
                u'<a href="{0}" target="_blank"><img style="object-fit: contain;" src="{0}" width="100" height="150"/></a>'.format(
                    self.photo.url))
        else:
            return '(Нет изображения)'

    show_image.short_description = 'Изображение'
    show_image.allow_tags = True


class CostIronRadiator(models.Model):
    class Meta:
        db_table = "Cost Iron Radiator"
        verbose_name = "Чугунный радиатор"
        verbose_name_plural = "Чугунные радиаторы"

    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель", default="")
    model_name = models.CharField("Модель", max_length=400)
    height = models.IntegerField("Высота")
    width = models.IntegerField("Ширина")
    depth = models.IntegerField("Глубина")
    center_distance = models.IntegerField("Межосевое расстояние")
    photo = models.ImageField("Картинка", blank=True, upload_to="cost_iron_images", default=None)
    description = models.TextField("Описание")
    power = models.CharField("Мощность (50 / 60 / 70)", max_length=120)
    pressure = models.IntegerField("Рабочее давление")
    weight = models.FloatField("Вес")
    price = models.FloatField("Цена", default=0)
    connection_type = models.ForeignKey(ConnectionType, on_delete=models.CASCADE, verbose_name="Тип подключения")

    def __str__(self):
        return self.model_name

    def show_image(self):
        if self.photo:
            return mark_safe(
                u'<a href="{0}" target="_blank"><img style="object-fit: contain;" src="{0}" width="100" height="150"/></a>'.format(
                    self.photo.url))
        else:
            return '(Нет изображения)'

    show_image.short_description = 'Изображение'
    show_image.allow_tags = True


class FloorConvector(models.Model):
    class Meta:
        db_table = "Floor Convector"
        verbose_name = "Напольный конвектор"
        verbose_name_plural = "Напольные конвекторы"

    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель")
    model_name = models.CharField("Модель", max_length=400)
    height = models.IntegerField("Высота")
    width = models.IntegerField("Ширина")
    length = models.IntegerField("Длина")
    photo = models.ImageField("Картинка", blank=True, upload_to="floor_convector_images", default=None)
    description = models.TextField("Описание")
    temperature = models.FloatField("Максимальная рабочая температура")
    pressure = models.FloatField("Максимальное рабочее давление")
    heat_output = models.FloatField("Выход тепла")
    surface_temperature = models.FloatField("Максимальная температура поверхности")
    connection = models.CharField("Подключение", max_length=200)
    price = models.FloatField("Цена", default=0)
    connection_type = models.ForeignKey(ConnectionType, on_delete=models.CASCADE, verbose_name="Тип подключения")

    def __str__(self):
        return self.model_name

    def show_image(self):
        if self.photo:
            return mark_safe(
                u'<a href="{0}" target="_blank"><img style="object-fit: contain;" src="{0}" width="100" height="150"/></a>'.format(
                    self.photo.url))
        else:
            return '(Нет изображения)'

    show_image.short_description = 'Изображение'
    show_image.allow_tags = True


class WallConvector(models.Model):
    class Meta:
        db_table = "Wall Convector"
        verbose_name = "Настенный конвектор"
        verbose_name_plural = "Настенные конвекторы"

    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель")
    model_name = models.CharField("Модель", max_length=400)
    height = models.IntegerField("Высота")
    width = models.IntegerField("Ширина")
    length = models.IntegerField("Длина")
    photo = models.ImageField("Картинка", blank=True, upload_to="wall_convector_images", default=None)
    description = models.TextField("Описание")
    temperature = models.FloatField("Максимальная рабочая температура")
    pressure = models.FloatField("Максимальное рабочее давление")
    heat_output = models.FloatField("Выход тепла")
    surface_temperature = models.FloatField("Максимальная температура поверхности")
    connection = models.CharField("Подключение", max_length=200)
    price = models.FloatField("Цена", default=0)
    connection_type = models.ForeignKey(ConnectionType, on_delete=models.CASCADE, verbose_name="Тип подключения")

    def __str__(self):
        return self.model_name

    def show_image(self):
        if self.photo:
            return mark_safe(
                u'<a href="{0}" target="_blank"><img style="object-fit: contain;" src="{0}" width="100" height="150"/></a>'.format(
                    self.photo.url))
        else:
            return '(Нет изображения)'

    show_image.short_description = 'Изображение'
    show_image.allow_tags = True


class RecessedConvector(models.Model):
    class Meta:
        db_table = "Recessed Convector"
        verbose_name = "Встраиваемый конвектор"
        verbose_name_plural = "Встраиваемые конвекторы"

    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель")
    model = models.ForeignKey(RecessedConvectorModel, verbose_name="Модель", on_delete=models.CASCADE)
    height = models.IntegerField("Высота, мм")
    width = models.IntegerField("Ширина, мм")
    length_unit = models.IntegerField("Единица длинны, мм", default=None)
    min_length = models.IntegerField("Минимальная длинна, мм", default=None)
    max_length = models.IntegerField("Максимальная длинна, мм", default=None)
    lattice = models.ForeignKey(LatticeType, verbose_name="Тип решетки", on_delete=models.CASCADE, default=None)
    side = models.ForeignKey(SideType, verbose_name="Тип бортика", on_delete=models.CASCADE, default=None)
    photo = models.ImageField("Картинка вид сверху", blank=True, upload_to="wall_convector_images", default=None)
    main_photo = models.ImageField("Общая картинка (вид в профиль)", blank=True, upload_to="wall_convector_images",
                                   default=None, null=True)
    description = models.TextField("Описание")
    price = models.FloatField("Цена за единицу длинны", default=0)
    connection_type = models.ForeignKey(ConnectionType, on_delete=models.CASCADE, verbose_name="Тип подключения")

    metal_thickness = models.FloatField("Толщина меттала, мм", null=True, default=None, blank=True)
    lattice_type = models.FloatField("Шаг ламелей решетки, мм", null=True, default=None, blank=True)
    presence_of_ribs = models.CharField("Наличие ребер жесткости", max_length=300, null=True, default=None, blank=True)
    temperature = models.FloatField("Максимальная рабочая температура", null=True, default=None, blank=True)
    pressure = models.FloatField("Максимальное рабочее давление", null=True, default=None, blank=True)
    heat_output = models.FloatField("Выход тепла", null=True, default=None, blank=True)
    surface_temperature = models.FloatField("Максимальная температура поверхности", null=True, default=None, blank=True)
    connection = models.CharField("Подключение", max_length=200, null=True, default=None, blank=True)

    def __str__(self):
        return f'{self.manufacturer.name} {self.model.name}'

    def show_image(self):
        if self.photo:
            return mark_safe(
                u'<a href="{0}" target="_blank"><img style="object-fit: contain;" src="{0}" width="100" height="150"/></a>'.format(
                    self.photo.url))
        else:
            return '(Нет изображения)'

    show_image.short_description = 'Изображение'
    show_image.allow_tags = True
