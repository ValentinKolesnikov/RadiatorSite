from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .choices import *
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json


def get_recessed_view_parms(manufacturer='', model='', side=''):
    radiators = RecessedConvector.objects.filter(manufacturer__name=manufacturer, model__name=model)
    args = {}
    sides_list = [{'name': radiator.side.name, 'image_url': radiator.photo.url} for radiator in radiators]
    lattices_list = [{'name': radiator.lattice.name, 'image_url': radiator.photo.url} for radiator in radiators if
                     radiator.side == side]
    args['sides'] = list({d['name']: d for d in sides_list}.values())
    args['lattices'] = list({d['name']: d for d in lattices_list}.values())
    return args


def get_list_information(radiators_count, radiators_class, radiator_type_id):
    manufacturers_descriptions = ManufacturerDescription.objects.filter(radiator_type=radiator_type_id)
    information = {'information': []}
    for manuf in manufacturers_descriptions:
        suitable_rads = radiators_class.objects.filter(manufacturer__name=manuf.manufacturer.name)[:radiators_count]
        temp = {'manufacturer_description': manuf,
                'widths': sorted(list(set([rad.width for rad in suitable_rads]))),
                'heights': sorted(list(set([rad.height for rad in suitable_rads])))}
        if (suitable_rads):
            information['information'].append(temp)
    return information


def search_in_components(search_string):
    suitable_comps = ComponentPart.objects.filter(name__icontains=search_string)
    return {'components_result': suitable_comps}


def search_in_aluminium(search_string):
    suitable_alum = AluminiumRadiator.objects.filter(
        Q(model_name__icontains=search_string) | Q(manufacturer__name__icontains=search_string))
    return {'radiators_result': suitable_alum}


def search_in_all_categories(search_string):
    # suitable_rad_cat = AluminiumRadiator.objects.filter(Q(name__icontains=search_string) | Q(manufacturer__name__icontains=search_string))
    suitable_comp_cat = ComponentType.objects.filter(name__icontains=search_string)
    return {'categories_result': suitable_comp_cat}


def clear_unnecessary_parameters(array, index):
    final_array = []
    for item in array:
        item = list(item)
        for i in range(0, len(item)):
            if i != index:
                item[i] = 0
        final_array.append(item)

    return final_array


def get_aluminium_radiator_parameters(radiator):
    args = {'manufacturers': [rad[0] for rad in AluminiumRadiator.objects.all().values_list('manufacturer__name')],
            'heights': radiator.height,
            'widths': radiator.width,
            'depths': radiator.depth,
            }

    return args


def get_suitable_options(params, radiator_tuples):
    args = {}
    suitable_radiators = []
    params_count = 0

    for i in params:
        if str(i) != '0':
            params_count += 1

    for index in range(0, params_count):
        if index == 0:
            for radiator in radiator_tuples:
                if str(params[index]) == str(radiator[index]):
                    suitable_radiators.append(radiator)
        elif suitable_radiators:
            temp = suitable_radiators.copy()
            for radiator in temp:
                if params[index] != radiator[index]:
                    suitable_radiators.remove(radiator)

    suitable_params = clear_unnecessary_parameters(suitable_radiators, params_count)
    args['manufacturers'] = sorted(list(set([rad[0] for rad in radiator_tuples])))
    args['parameters'] = sorted(list(set([rad[params_count] for rad in suitable_params if rad[params_count]])))
    return args


def get_first_suitable_rad(params=[], all_radiators=[]):
    suitable_radiator = []
    params_count = 0

    for i in params:
        if str(i) != '0':
            params_count += 1

    for rad in all_radiators:
        count = 0
        for i in range(0, params_count):
            if rad[i] == params[i]:
                count += 1
        if count == params_count:
            suitable_radiator = rad
            break

    return suitable_radiator


def get_components_for_see_also(count):
    return ComponentPart.objects.order_by('?')[:count]


@csrf_exempt
def aluminium_view(request):
    args = {}
    post_data = request.POST
    args['components'] = get_components_for_see_also(4)

    if request.method == "POST" and post_data.get('parameters'):
        tuples_for_options = AluminiumRadiator.objects.all().values_list('manufacturer__name', 'height', 'width',
                                                                         'depth',
                                                                         'center_distance', 'connection_type__name')
        params = json.loads(post_data.get('parameters'))
        option_id = post_data.get('optionID')
        unit = post_data.get('unit')

        args.update(get_suitable_options(params, tuples_for_options))
        args['option_id'] = option_id
        args['unit'] = unit

        return render(request, 'catalog/includes/options.html', args)

    elif request.method == "POST" and post_data.get('radiatorOptions'):
        tuples_for_radiator_search = AluminiumRadiator.objects.all().values_list('manufacturer__name', 'height',
                                                                                 'width',
                                                                                 'depth',
                                                                                 'center_distance',
                                                                                 'connection_type__name',
                                                                                 'id')
        options = json.loads(post_data.get('radiatorOptions'))
        suitable_radiator = get_first_suitable_rad(options, tuples_for_radiator_search)
        if suitable_radiator:
            suitable_radiator = AluminiumRadiator.objects.get(id=suitable_radiator[6])
        args['radiator'] = suitable_radiator
        args['manufacturers'] = list(
            set([rad[0] for rad in AluminiumRadiator.objects.all().values_list('manufacturer__name')]))
        return render(request, 'catalog/filters/aluminium.html', args)

    elif request.method == "GET":
        try:
            rads = AluminiumRadiator.objects.all()[0]
        except IndexError:
            args['ex_title'] = "404 Not Found"
            args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
            return render(request, "mainApp/404.html", args)
        args['radiator'] = rads
        args['components'] = ComponentPart.objects.order_by('?')[:4]
        args['manufacturers'] = list(
            set([rad[0] for rad in AluminiumRadiator.objects.all().values_list('manufacturer__name')]))

        return render(request, 'catalog/filters/aluminium.html', args)


@csrf_exempt
def search_view(request):
    if request.method == "POST":
        args = {}
        search_string = request.POST.get('search_string')
        args.update(search_in_all_categories(search_string))
        args.update(search_in_aluminium(search_string))
        args.update(search_in_components(search_string))

        return render(request, 'mainApp/search.html', args)


@csrf_exempt
def bimetal_view(request):
    args = {}
    post_data = request.POST
    args['components'] = get_components_for_see_also(4)

    if request.method == "POST" and post_data.get('parameters'):
        tuples_for_options = BimetalRadiator.objects.all().values_list('manufacturer__name', 'height', 'width',
                                                                       'depth',
                                                                       'center_distance', 'connection_type__name')
        params = json.loads(post_data.get('parameters'))
        option_id = post_data.get('optionID')
        unit = post_data.get('unit')

        args.update(get_suitable_options(params, tuples_for_options))
        args['option_id'] = option_id
        args['unit'] = unit

        return render(request, 'catalog/includes/options.html', args)

    elif request.method == "POST" and post_data.get('radiatorOptions'):
        tuples_for_radiator_search = BimetalRadiator.objects.all().values_list('manufacturer__name', 'height',
                                                                               'width',
                                                                               'depth',
                                                                               'center_distance',
                                                                               'connection_type__name',
                                                                               'id')
        options = json.loads(post_data.get('radiatorOptions'))
        suitable_radiator = get_first_suitable_rad(options, tuples_for_radiator_search)
        if suitable_radiator:
            suitable_radiator = BimetalRadiator.objects.get(id=suitable_radiator[6])
        args['radiator'] = suitable_radiator
        args['manufacturers'] = list(
            set([rad[0] for rad in BimetalRadiator.objects.all().values_list('manufacturer__name')]))
        return render(request, 'catalog/filters/bimetal.html', args)

    elif request.method == "GET":
        try:
            rads = BimetalRadiator.objects.all()[0]
        except IndexError:
            args['ex_title'] = "404 Not Found"
            args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
            return redirect("404.html", args)
        args['radiator'] = rads
        args['manufacturers'] = list(
            set([rad[0] for rad in BimetalRadiator.objects.all().values_list('manufacturer__name')]))
        return render(request, 'catalog/filters/bimetal.html', args)


@csrf_exempt
def design_view(request, manufacturer_id=''):
    args = {}
    post_data = request.POST
    args['components'] = get_components_for_see_also(4)

    if request.method == "POST" and post_data.get('parameters'):
        tuples_for_options = DesignRadiator.objects.all().values_list('manufacturer__name', 'height', 'width')
        params = json.loads(post_data.get('parameters'))
        option_id = post_data.get('optionID')
        unit = post_data.get('unit')

        args.update(get_suitable_options(params, tuples_for_options))
        args['option_id'] = option_id
        args['unit'] = unit

        return render(request, 'catalog/includes/options.html', args)

    elif request.method == "POST" and post_data.get('radiatorOptions'):
        tuples_for_radiator_search = DesignRadiator.objects.all().values_list('manufacturer__name', 'height', 'width',
                                                                              'id')
        options = json.loads(post_data.get('radiatorOptions'))
        suitable_radiator = get_first_suitable_rad(options, tuples_for_radiator_search)
        if suitable_radiator:
            suitable_radiator = DesignRadiator.objects.get(id=suitable_radiator[3])
        args['radiator'] = suitable_radiator
        args['manufacturers'] = list(
            set([rad[0] for rad in DesignRadiator.objects.all().values_list('manufacturer__name')]))
        return render(request, 'catalog/filters/design.html', args)

    elif request.method == "GET":
        try:
            rad = DesignRadiator.objects.filter(manufacturer__id=manufacturer_id)[0]
        except IndexError:
            args['ex_title'] = "404 Not Found"
            args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
            return redirect("404.html", args)
        args['radiator'] = rad
        args['manufacturers'] = list(
            set([rad[0] for rad in DesignRadiator.objects.all().values_list('manufacturer__name')]))
        return render(request, 'catalog/filters/design.html', args)


@csrf_exempt
def steel_panel_view(request):
    args = {}
    post_data = request.POST
    args['components'] = get_components_for_see_also(4)

    if request.method == "POST" and post_data.get('parameters'):
        tuples_for_options = SteelPanelRadiator.objects.all().values_list('manufacturer__name', 'height', 'width',
                                                                          'depth',
                                                                          'center_distance', 'connection_type__name')
        params = json.loads(post_data.get('parameters'))
        option_id = post_data.get('optionID')
        unit = post_data.get('unit')

        args.update(get_suitable_options(params, tuples_for_options))
        args['option_id'] = option_id
        args['unit'] = unit

        return render(request, 'catalog/includes/options.html', args)

    elif request.method == "POST" and post_data.get('radiatorOptions'):
        tuples_for_radiator_search = SteelPanelRadiator.objects.all().values_list('manufacturer__name', 'height',
                                                                                  'width',
                                                                                  'depth',
                                                                                  'center_distance',
                                                                                  'connection_type__name',
                                                                                  'id')
        options = json.loads(post_data.get('radiatorOptions'))
        suitable_radiator = get_first_suitable_rad(options, tuples_for_radiator_search)
        if suitable_radiator:
            suitable_radiator = SteelPanelRadiator.objects.get(id=suitable_radiator[6])
        args['radiator'] = suitable_radiator
        args['manufacturers'] = list(
            set([rad[0] for rad in SteelPanelRadiator.objects.all().values_list('manufacturer__name')]))
        return render(request, 'catalog/filters/steel-panel.html', args)

    elif request.method == "GET":
        try:
            rad = SteelPanelRadiator.objects.all()[0]
        except IndexError:
            args['ex_title'] = "404 Not Found"
            args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
            return render(request, "mainApp/404.html", args)
        args['radiator'] = rad
        args['manufacturers'] = list(
            set([rad[0] for rad in SteelPanelRadiator.objects.all().values_list('manufacturer__name')]))

        return render(request, 'catalog/filters/steel-panel.html', args)


@csrf_exempt
def steel_tubular_view(request):
    args = {}
    post_data = request.POST
    args['components'] = get_components_for_see_also(4)

    if request.method == "POST" and post_data.get('parameters'):
        tuples_for_options = 0
        params = json.loads(post_data.get('parameters'))
        option_id = post_data.get('optionID')
        unit = post_data.get('unit')
        tuples_for_options = SteelTubularRadiator.objects.all().values_list('manufacturer__name', 'height', 'width',
                                                                            'depth', 'connection_type__name')

        args.update(get_suitable_options(params, tuples_for_options))
        args['option_id'] = option_id
        args['unit'] = unit

        return render(request, 'catalog/includes/options.html', args)

    elif request.method == "POST" and post_data.get('radiatorOptions'):

        options = json.loads(post_data.get('radiatorOptions'))

        tuples_for_radiator_search = SteelTubularRadiator.objects.all().values_list('manufacturer__name', 'height',
                                                                                    'width',
                                                                                    'depth', 'connection_type__name',
                                                                                    'id')
        suitable_radiator = get_first_suitable_rad(options, tuples_for_radiator_search)
        if suitable_radiator:
            suitable_radiator = SteelTubularRadiator.objects.get(id=suitable_radiator[5])
        args['radiator'] = suitable_radiator

        args['manufacturers'] = list(
            set([rad[0] for rad in SteelTubularRadiator.objects.all().values_list('manufacturer__name')]))

        return render(request, 'catalog/filters/steel-tubular.html', args)


    elif request.method == "GET":
        try:
            rad = SteelTubularRadiator.objects.all()[0]
        except IndexError:
            args['ex_title'] = "404 Not Found"
            args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
            return render(request, "mainApp/404.html", args)
        args['radiator'] = rad
        args['manufacturers'] = list(
            set([rad[0] for rad in SteelTubularRadiator.objects.all().values_list('manufacturer__name')]))

        return render(request, 'catalog/filters/steel-tubular.html', args)


@csrf_exempt
def steel_tubular_kzto_view(request):
    args = {}
    post_data = request.POST
    args['components'] = get_components_for_see_also(4)

    if request.method == "POST" and post_data.get('parameters'):
        params = json.loads(post_data.get('parameters'))
        option_id = post_data.get('optionID')
        unit = post_data.get('unit')
        tuples_for_options = SteelTubularKZTORadiator.objects.all().values_list('manufacturer_name',
                                                                                'appliance_type__name', 'length',
                                                                                'mounting_size',
                                                                                'connection_type__name')

        args.update(get_suitable_options(params, tuples_for_options))
        args['option_id'] = option_id
        args['unit'] = unit

        return render(request, 'catalog/includes/options.html', args)

    elif request.method == "POST" and post_data.get('radiatorOptions'):

        options = json.loads(post_data.get('radiatorOptions'))

        tuples_for_radiator_search = SteelTubularKZTORadiator.objects.all().values_list('manufacturer_name',
                                                                                        'appliance_type__name',
                                                                                        'length', 'mounting_size',
                                                                                        'connection_type__name', 'id')
        suitable_radiator = get_first_suitable_rad(options, tuples_for_radiator_search)
        if suitable_radiator:
            suitable_radiator = SteelTubularKZTORadiator.objects.get(id=suitable_radiator[5])

        args['radiator'] = suitable_radiator
        args['manufacturers'] = list(
            set([rad[0] for rad in SteelTubularRadiator.objects.all().values_list('manufacturer__name')]))

        return render(request, 'catalog/filters/steel-tubular-kzto.html', args)

    elif request.method == "GET":
        try:
            rad = SteelTubularKZTORadiator.objects.all()[0]
        except IndexError:
            args['ex_title'] = "404 Not Found"
            args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
            return render(request, "mainApp/404.html", args)
        args['radiator'] = rad
        args['manufacturers'] = list(
            set([rad[0] for rad in SteelTubularRadiator.objects.all().values_list('manufacturer__name')]))

        return render(request, 'catalog/filters/steel-tubular-kzto.html', args)


@csrf_exempt
def cost_iron_view(request, manufacturer_id=''):
    args = {}
    post_data = request.POST
    args['components'] = get_components_for_see_also(4)

    if request.method == "POST" and post_data.get('parameters'):
        tuples_for_options = CostIronRadiator.objects.all().values_list('manufacturer__name', 'height', 'width',
                                                                        'depth',
                                                                        'center_distance', 'connection_type__name')
        params = json.loads(post_data.get('parameters'))
        option_id = post_data.get('optionID')
        unit = post_data.get('unit')

        args.update(get_suitable_options(params, tuples_for_options))
        args['option_id'] = option_id
        args['unit'] = unit

        return render(request, 'catalog/includes/options.html', args)

    elif request.method == "POST" and post_data.get('radiatorOptions'):
        tuples_for_radiator_search = CostIronRadiator.objects.all().values_list('manufacturer__name', 'height', 'width',
                                                                                'depth',
                                                                                'center_distance',
                                                                                'connection_type__name',
                                                                                'id')
        options = json.loads(post_data.get('radiatorOptions'))
        suitable_radiator = get_first_suitable_rad(options, tuples_for_radiator_search)
        if suitable_radiator:
            suitable_radiator = CostIronRadiator.objects.get(id=suitable_radiator[6])
        args['radiator'] = suitable_radiator
        args['manufacturers'] = list(
            set([rad[0] for rad in CostIronRadiator.objects.all().values_list('manufacturer__name')]))
        return render(request, 'catalog/filters/cost-iron.html', args)

    elif request.method == "GET":
        try:
            rads = CostIronRadiator.objects.filter(manufacturer__id=manufacturer_id)[0]
        except IndexError:
            args['ex_title'] = "404 Not Found"
            args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
            return render(request, "mainApp/404.html", args)
        args['radiator'] = rads
        args['components'] = ComponentPart.objects.order_by('?')[:4]
        args['manufacturers'] = list(
            set([rad[0] for rad in CostIronRadiator.objects.all().values_list('manufacturer__name')]))

        return render(request, 'catalog/filters/cost-iron.html', args)


@csrf_exempt
def floor_convector_view(request, manufacturer_id):
    args = {}
    post_data = request.POST
    args['components'] = get_components_for_see_also(4)

    if request.method == "POST" and post_data.get('parameters'):
        tuples_for_options = FloorConvector.objects.all().values_list('manufacturer__name', 'height', 'width',
                                                                      'length', 'connection_type__name')
        params = json.loads(post_data.get('parameters'))
        option_id = post_data.get('optionID')
        unit = post_data.get('unit')

        args.update(get_suitable_options(params, tuples_for_options))
        args['option_id'] = option_id
        args['unit'] = unit

        return render(request, 'catalog/includes/options.html', args)

    elif request.method == "POST" and post_data.get('radiatorOptions'):
        tuples_for_radiator_search = FloorConvector.objects.all().values_list('manufacturer__name', 'height', 'width',
                                                                              'length', 'connection_type__name',
                                                                              'id')
        options = json.loads(post_data.get('radiatorOptions'))
        suitable_radiator = get_first_suitable_rad(options, tuples_for_radiator_search)
        if suitable_radiator:
            suitable_radiator = FloorConvector.objects.get(id=suitable_radiator[5])
        args['radiator'] = suitable_radiator
        args['manufacturers'] = list(
            set([rad[0] for rad in FloorConvector.objects.all().values_list('manufacturer__name')]))
        return render(request, 'catalog/filters/floor_convector.html', args)

    elif request.method == "GET":
        try:
            rads = FloorConvector.objects.filter(manufacturer__id=manufacturer_id)[0]
        except IndexError:
            args['ex_title'] = "404 Not Found"
            args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
            return render(request, "mainApp/404.html", args)
        args['radiator'] = rads
        args['components'] = ComponentPart.objects.order_by('?')[:4]
        args['manufacturers'] = list(
            set([rad[0] for rad in FloorConvector.objects.all().values_list('manufacturer__name')]))

        return render(request, 'catalog/filters/floor_convector.html', args)


@csrf_exempt
def wall_convector_view(request, manufacturer_id):
    args = {}
    post_data = request.POST
    args['components'] = get_components_for_see_also(4)

    if request.method == "POST" and post_data.get('parameters'):
        tuples_for_options = WallConvector.objects.all().values_list('manufacturer__name', 'height', 'width',
                                                                     'length', 'connection_type__name')
        params = json.loads(post_data.get('parameters'))
        option_id = post_data.get('optionID')
        unit = post_data.get('unit')

        args.update(get_suitable_options(params, tuples_for_options))
        args['option_id'] = option_id
        args['unit'] = unit

        return render(request, 'catalog/includes/options.html', args)

    elif request.method == "POST" and post_data.get('radiatorOptions'):
        tuples_for_radiator_search = WallConvector.objects.all().values_list('manufacturer__name', 'height', 'width',
                                                                             'length', 'connection_type__name',
                                                                             'id')
        options = json.loads(post_data.get('radiatorOptions'))
        suitable_radiator = get_first_suitable_rad(options, tuples_for_radiator_search)
        if suitable_radiator:
            suitable_radiator = WallConvector.objects.get(id=suitable_radiator[5])
        args['radiator'] = suitable_radiator
        args['manufacturers'] = list(
            set([rad[0] for rad in WallConvector.objects.all().values_list('manufacturer__name')]))
        return render(request, 'catalog/filters/wall_convector.html', args)

    elif request.method == "GET":
        try:
            rads = WallConvector.objects.filter(manufacturer__id=manufacturer_id)[0]
        except IndexError:
            args['ex_title'] = "404 Not Found"
            args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
            return render(request, "mainApp/404.html", args)
        args['radiator'] = rads
        args['components'] = ComponentPart.objects.order_by('?')[:4]
        args['manufacturers'] = list(
            set([rad[0] for rad in WallConvector.objects.all().values_list('manufacturer__name')]))

        return render(request, 'catalog/filters/wall_convector.html', args)


@csrf_exempt
def recessed_convector_view(request, manufacturer_id):
    args = {}
    post_data = request.POST
    args['components'] = get_components_for_see_also(4)

    if request.method == "POST" and post_data.get('parameters'):
        tuples_for_options = RecessedConvector.objects.all().values_list('manufacturer__name', 'model__name',
                                                                         'side__name',
                                                                         'lattice__name', 'height', 'width',
                                                                         'connection_type__name')
        params = json.loads(post_data.get('parameters'))
        option_id = post_data.get('optionID')
        unit = post_data.get('unit')

        args.update(get_suitable_options(params, tuples_for_options))
        args['option_id'] = option_id
        args['unit'] = unit

        return render(request, 'catalog/includes/options.html', args)

    elif request.method == "POST" and post_data.get('side'):

        tuples_for_radiator_search = RecessedConvector.objects.all().values_list('manufacturer__name', 'model__name',
                                                                                 'side__name',
                                                                                 'lattice__name', 'id')
        if (post_data.get('lattice') == ''):
            options = [post_data.get('manufacturer'), post_data.get('model'), post_data.get('side'),
                       RecessedConvector.objects.filter(side__name=post_data.get('side'))[0].lattice.name]
        else:
            options = [post_data.get('manufacturer'), post_data.get('model'), post_data.get('side'),
                       post_data.get('lattice')]
        suitable_radiator = get_first_suitable_rad(options, tuples_for_radiator_search)
        if suitable_radiator:
            suitable_radiator = RecessedConvector.objects.get(id=suitable_radiator[4])
        args['radiator'] = suitable_radiator

        args['default_price'] = suitable_radiator.price * suitable_radiator.min_length
        args['manufacturers'] = list(
            set([rad[0] for rad in RecessedConvector.objects.all().values_list('manufacturer__name')]))
        args['models'] = list(
            set([radiator.model for radiator in
                 RecessedConvector.objects.filter(manufacturer__id=suitable_radiator.manufacturer.id)]))
        args.update(get_recessed_view_parms(manufacturer=suitable_radiator.manufacturer, model=suitable_radiator.model,
                                            side=suitable_radiator.side))

        return render(request, 'catalog/filters/recessed_convector.html', args)

    elif request.method == "POST" and post_data.get('radiatorOptions'):
        tuples_for_radiator_search = RecessedConvector.objects.all().values_list('manufacturer__name', 'model__name',
                                                                                 'side__name',
                                                                                 'lattice__name', 'height', 'width',
                                                                                 'connection_type__name',
                                                                                 'id')
        options = json.loads(post_data.get('radiatorOptions'))
        suitable_radiator = get_first_suitable_rad(options, tuples_for_radiator_search)
        if suitable_radiator:
            suitable_radiator = RecessedConvector.objects.get(id=suitable_radiator[7])
        args['radiator'] = suitable_radiator
        args['default_price'] = suitable_radiator.price * suitable_radiator.min_length
        args['manufacturers'] = list(
            set([rad[0] for rad in RecessedConvector.objects.all().values_list('manufacturer__name')]))
        args['models'] = list(
            set([radiator.model for radiator in
                 RecessedConvector.objects.filter(manufacturer__id=suitable_radiator.manufacturer.id)]))
        args.update(get_recessed_view_parms(manufacturer=suitable_radiator.manufacturer, model=suitable_radiator.model,
                                            side=suitable_radiator.side))
        return render(request, 'catalog/filters/recessed_convector.html', args)

    elif request.method == "GET":
        try:
            rad = RecessedConvector.objects.filter(manufacturer__id=manufacturer_id)[0]
        except IndexError:
            args['ex_title'] = "404 Not Found"
            args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
            return render(request, "mainApp/404.html", args)
        args['radiator'] = rad
        args['default_price'] = rad.price * rad.min_length
        args['models'] = list(
            set([radiator.model for radiator in RecessedConvector.objects.filter(manufacturer__id=manufacturer_id)]))
        args['manufacturers'] = list(
            set([rad[0] for rad in RecessedConvector.objects.all().values_list('manufacturer__name')]))
        args.update(get_recessed_view_parms(manufacturer=rad.manufacturer, model=rad.model, side=rad.side))

        return render(request, 'catalog/filters/recessed_convector.html', args)


def components_list_view(request):
    args = {'all_categories': ComponentType.objects.all()}
    return render(request, 'catalog/categories_lists/components-categories.html', args)


def component_type_list_view(request, component_type_id=None):
    if component_type_id:
        components = ComponentPart.objects.filter(type_id=component_type_id)
        args = {'components': components}
        return render(request, 'catalog/lists/component-parts.html', args)
    else:
        pass


def component_page_view(request, component_type_id=None, component_id=None):
    if component_id:
        args = {'component': ComponentPart.objects.filter(id=component_id)[0]}
        return render(request, "catalog/pages/component-part-page.html", args)
    else:
        pass


def design_list_view(request):
    args = get_list_information(radiators_count=3, radiators_class=DesignRadiator, radiator_type_id=1)
    return render(request, 'catalog/lists/design.html', args)


def cost_iron_list_view(request):
    args = get_list_information(radiators_count=3, radiators_class=CostIronRadiator, radiator_type_id=2)
    return render(request, 'catalog/lists/cost-iron.html', args)


def convector_categories_view(request):
    return render(request, 'catalog/categories_lists/convector.html')


def floor_convector_list_view(request):
    args = get_list_information(radiators_count=3, radiators_class=FloorConvector, radiator_type_id=4)
    return render(request, 'catalog/lists/floor_convector.html', args)


def wall_convector_list_view(request):
    args = get_list_information(radiators_count=3, radiators_class=WallConvector, radiator_type_id=5)
    return render(request, 'catalog/lists/wall_convector.html', args)


def recessed_convector_list_view(request):
    args = get_list_information(radiators_count=3, radiators_class=RecessedConvector, radiator_type_id=3)
    return render(request, 'catalog/lists/wall_convector.html', args)
