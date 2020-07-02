from django.contrib import admin
from .models import *


class ComponentPartAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'show_image')
    list_filter = ['type']


class AluminiumAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'manufacturer', 'show_image')
    list_filter = ['manufacturer']


class BimetalAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'manufacturer', 'show_image')
    list_filter = ['manufacturer']


class DesignAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'manufacturer', 'show_image')
    list_filter = ['manufacturer']


class SteelPanelAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'manufacturer', 'show_image')
    list_filter = ['manufacturer']

class SteelTubularAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'manufacturer', 'show_image')
    list_filter = ['manufacturer']

class SteelTubularKZTOAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'show_image')

class CostIronAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'manufacturer', 'show_image')
    list_filter = ['manufacturer']


class FloorConvectorAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'manufacturer', 'show_image')
    list_filter = ['manufacturer']


class WallConvectorAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'manufacturer', 'show_image')
    list_filter = ['manufacturer']

class RecessedConvectorAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'model', 'show_image')
    list_filter = ['manufacturer']

class ManufacturerDescriptionAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'radiator_type', 'description', 'show_image')
    list_filter = ['manufacturer']

admin.site.register(ConnectionType)
admin.site.register(Manufacturer)
admin.site.register(ManufacturerDescription, ManufacturerDescriptionAdmin)
admin.site.register(AluminiumRadiator, AluminiumAdmin)
admin.site.register(BimetalRadiator, BimetalAdmin)
admin.site.register(DesignRadiator, DesignAdmin)
admin.site.register(CostIronRadiator, CostIronAdmin)
admin.site.register(SteelPanelRadiator, SteelPanelAdmin)
admin.site.register(SteelTubularRadiator, SteelTubularAdmin)
admin.site.register(SteelTubularKZTORadiator, SteelTubularKZTOAdmin)
admin.site.register(FloorConvector, FloorConvectorAdmin)
admin.site.register(WallConvector, WallConvectorAdmin)
admin.site.register(RecessedConvector, RecessedConvectorAdmin)
admin.site.register(ComponentPart, ComponentPartAdmin)
admin.site.register(ComponentType)
admin.site.register(ApplianceType)
admin.site.register(LatticeType)
admin.site.register(RecessedConvectorModel)
admin.site.register(SideType)
admin.site.register(Color)



