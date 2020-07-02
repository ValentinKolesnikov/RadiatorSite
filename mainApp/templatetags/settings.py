from django import template
from mainApp.models import SiteSettings

register = template.Library()

@register.simple_tag
def get_settings(name):
    settings = ''
    try:
        settings = SiteSettings.objects.filter()[0]
    except:
        settings = SiteSettings(name='Радиаторы', phone='+375 33 475 53 35', mail='test@gmail.com', address='example')
        settings.save()
    if name == "name":
        return settings.name
    if name == "phone":
        return settings.phone
    if name == "address":
        return settings.address
    if name == "mail":
        return settings.mail