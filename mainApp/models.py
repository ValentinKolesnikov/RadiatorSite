from django.core.exceptions import ValidationError
from django.db import models


class SiteSettings(models.Model):
    class Meta:
        db_table = "Site Settings"
        verbose_name = "Параметры сайта"
        verbose_name_plural = "Параметры сайта"

    name = models.CharField('Название сайта', max_length=100)
    phone = models.CharField('Телефон', max_length=40)
    mail = models.CharField('Email', max_length=200)
    address = models.CharField('Адрес', max_length=300)

    def save(self, *args, **kwargs):
        if SiteSettings.objects.exists() and not self.pk:
            raise ValidationError('Вы можете создать только один экземпляр SiteSettings')
        return super(SiteSettings, self).save(*args, **kwargs)
