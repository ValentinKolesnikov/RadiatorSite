from django.urls import path, include
from . import views

urlpatterns = [
    path('main-search', views.search_view, name="search_view"),
    path('radiators/aluminium', views.aluminium_view, name="aluminium_view"),
    path('radiators/aluminium/<int:id>', views.aluminium_view, name="aluminium_view"),
    path('radiators/bimetal', views.bimetal_view, name="bimetal_view"),
    path('radiators/bimetal/<int:id>', views.bimetal_view, name="bimetal_view"),
    path('radiators/steel-panel', views.steel_panel_view, name="steel_panel_view"),
    path('radiators/steel-panel/<int:id>', views.steel_panel_view, name="steel_panel_view"),
    path('radiators/steel-tubular', views.steel_tubular_view, name="steel_tubular_view"),
    path('radiators/steel-tubular/<int:id>', views.steel_tubular_view, name="steel_tubular_view"),
    path('radiators/steel-tubular/kzto', views.steel_tubular_kzto_view, name="steel_tubular_kzto_view"),
    path('radiators/steel-tubular/kzto/<int:id>', views.steel_tubular_kzto_view, name="steel_tubular_kzto_view"),
    path('radiators/design-list', views.design_list_view, name="design_list_view"),
    path('radiators/cost-iron-list', views.cost_iron_list_view, name="cost_iron_list_view"),
    path('radiators/design/<int:manufacturer_id>', views.design_view, name="design_view"),
    path('radiators/design/<int:manufacturer_id>/<int:id>', views.design_view, name="design_view"),
    path('radiators/cost-iron/<int:manufacturer_id>', views.cost_iron_view, name="cost_iron_view"),
    path('radiators/cost-iron/<int:manufacturer_id>/<int:id>', views.cost_iron_view, name="cost_iron_view"),
    path('radiators/convector-categories', views.convector_categories_view, name="convector_categories_view"),
    path('radiators/convector-categories/floor', views.floor_convector_list_view, name="floor_convector_list_view"),
    path('radiators/convector-categories/floor/<int:manufacturer_id>', views.floor_convector_view,
         name="floor_convector_view"),
    path('radiators/convector-categories/floor/<int:manufacturer_id>/<int:id>', views.floor_convector_view,
         name="floor_convector_view"),
    path('radiators/convector-categories/wall', views.wall_convector_list_view, name="wall_convector_list_view"),
    path('radiators/convector-categories/wall/<int:manufacturer_id>', views.wall_convector_view,
         name="wall_convector_view"),
    path('radiators/convector-categories/wall/<int:manufacturer_id>/<int:id>', views.wall_convector_view,
         name="wall_convector_view"),
    path('radiators/convector-categories/recessed', views.recessed_convector_list_view,
         name="recessed_convector_list_view"),
    path('radiators/convector-categories/recessed/<int:manufacturer_id>', views.recessed_convector_view,
         name="recessed_convector_view"),
    path('radiators/convector-categories/recessed/<int:manufacturer_id>/<int:id>', views.recessed_convector_view,
         name="recessed_convector_view"),
    path('component-parts/', views.components_list_view, name="components_list_view"),
    path('component-parts/<int:component_type_id>/', views.component_type_list_view, name="component_type_list_view"),
    path('component-parts/<int:component_type_id>/<int:component_id>', views.component_page_view,
         name="component_page_view"),

]
