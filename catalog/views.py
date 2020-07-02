import json

from django.db.models import Q
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import *


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


def search_in_model_class(class_name, class_link, items_list, search_string):
    args = {}
    temp = []
    for j in items_list:
        full_name = f'{j[0]} {j[1]}'.lower()
        if full_name.rfind(search_string.lower()) != -1:
            temp.append(class_link.objects.get(id=j[2]))
    args[class_name] = temp[:2]
    return args


def search_in_categories(search_string):
    args = {}
    for key in RADIATOR_CLASSES_NAMES:
        if RADIATOR_CLASSES_NAMES[key].find(search_string.lower()) != -1:
            args[key] = True
    return args

def search_in_all_list(search_string):

    classes = [AluminiumRadiator, BimetalRadiator, DesignRadiator, CostIronRadiator, SteelPanelRadiator,
               SteelTubularRadiator, FloorConvector, WallConvector]
    names = ['aluminium', 'bimetal', 'design', 'cost_iron', 'steel_panel', 'steel_tubular', 'floor', 'wall']
    args = {}

    for i in range(0, len(names)):
        all = classes[i].objects.values_list('manufacturer__name', 'model_name', 'id')
        args.update(search_in_model_class(names[i], classes[i], all, search_string))

    all = SteelTubularKZTORadiator.objects.values_list('manufacturer_name', 'model_name', 'id')
    args.update(search_in_model_class('steel_tubular_kzto', SteelTubularKZTORadiator, all, search_string))

    all = RecessedConvector.objects.values_list('manufacturer__name', 'model__name', 'id')
    args.update(search_in_model_class('recessed', RecessedConvector, all, search_string))

    return args



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


def find_coincidences_aluminium_similar(radiator, class_name, request):
    args = {}
    try:
        coincidences = class_name.objects.filter(manufacturer=radiator.manufacturer,
                                                 width=radiator.width, depth=radiator.depth,
                                                 height=radiator.height,
                                                 center_distance=radiator.center_distance,
                                                 connection_type=radiator.connection_type)
    except class_name.DoesNotExist:
        args['ex_title'] = "404 Not Found"
        args['ex_text'] = "В каталоге не найдено подходящего радиатора данной категории"
        return render(request, "mainApp/404.html", args)
    except IndexError:
        args['ex_title'] = "404 Not Found"
        args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
        return render(request, "mainApp/404.html", args)
    return coincidences


def find_coincidences_design(radiator, request):
    args = {}
    try:
        coincidences = DesignRadiator.objects.filter(manufacturer=radiator.manufacturer, width=radiator.width,
                                                     height=radiator.height)
    except IndexError or DesignRadiator.DoesNotExist:
        args['ex_title'] = "404 Not Found"
        args['ex_text'] = "В каталоге не найдено подходящего радиатора данной категории"
        return render(request, "mainApp/404.html", args)
    except IndexError:
        args['ex_title'] = "404 Not Found"
        args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
        return render(request, "mainApp/404.html", args)
    return coincidences


def find_coincidences_steel_tubular(radiator, request):
    args = {}
    try:
        coincidences = SteelTubularRadiator.objects.filter(manufacturer=radiator.manufacturer,
                                                           width=radiator.width, depth=radiator.depth,
                                                           height=radiator.height,
                                                           connection_type=radiator.connection_type)
    except SteelTubularRadiator.DoesNotExist:
        args['ex_title'] = "404 Not Found"
        args['ex_text'] = "В каталоге не найдено подходящего радиатора данной категории"
        return render(request, "mainApp/404.html", args)
    except IndexError:
        args['ex_title'] = "404 Not Found"
        args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
        return render(request, "mainApp/404.html", args)
    return coincidences


def find_coincidences_steel_tubular_kzto(radiator, request):
    args = {}
    try:
        coincidences = SteelTubularKZTORadiator.objects.filter(manufacturer_name=radiator.manufacturer_name,
                                                               appliance_type=radiator.appliance_type,
                                                               length=radiator.length,
                                                               mounting_size=radiator.mounting_size,
                                                               connection_type=radiator.connection_type)
    except SteelTubularKZTORadiator.DoesNotExist:
        args['ex_title'] = "404 Not Found"
        args['ex_text'] = "В каталоге не найдено подходящего радиатора данной категории"
        return render(request, "mainApp/404.html", args)
    except IndexError:
        args['ex_title'] = "404 Not Found"
        args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
        return render(request, "mainApp/404.html", args)
    return coincidences


def find_coincidences_floor_similar(radiator, class_name, request):
    args = {}
    try:
        coincidences = class_name.objects.filter(manufacturer=radiator.manufacturer,
                                                           width=radiator.width, length=radiator.length,
                                                           height=radiator.height,
                                                           connection_type=radiator.connection_type)
    except class_name.DoesNotExist:
        args['ex_title'] = "404 Not Found"
        args['ex_text'] = "В каталоге не найдено подходящего радиатора данной категории"
        return render(request, "mainApp/404.html", args)
    except IndexError:
        args['ex_title'] = "404 Not Found"
        args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
        return render(request, "mainApp/404.html", args)
    return coincidences


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
def aluminium_view(request, id=-1):
    args = {}
    post_data = request.POST
    args['components'] = get_components_for_see_also(4)

    tuples_for_radiator_search = AluminiumRadiator.objects.all().values_list('manufacturer__name', 'width', 'depth',
                                                                             'height', 'center_distance',
                                                                             'connection_type__name', 'id')
    if request.method == "POST" and post_data.get('parameters'):
        tuples_for_options = AluminiumRadiator.objects.all().values_list('manufacturer__name', 'width',
                                                                         'depth', 'height', 'center_distance',
                                                                         'connection_type__name')
        params = json.loads(post_data.get('parameters'))
        option_id = post_data.get('optionID')
        unit = post_data.get('unit')

        args.update(get_suitable_options(params, tuples_for_options))
        args['option_id'] = option_id
        args['unit'] = unit

        return render(request, 'catalog/includes/options.html', args)

    elif request.method == "POST" and post_data.get('radiatorOptions'):

        options = json.loads(post_data.get('radiatorOptions'))
        suitable_radiator = get_first_suitable_rad(options, tuples_for_radiator_search)
        if suitable_radiator:
            suitable_radiator = AluminiumRadiator.objects.get(id=suitable_radiator[6])
        args['radiator'] = suitable_radiator
        args['manufacturers'] = list(
            set([rad[0] for rad in AluminiumRadiator.objects.all().values_list('manufacturer__name')]))
        coincidences = find_coincidences_aluminium_similar(suitable_radiator, AluminiumRadiator, request)
        args['coincidences'] = '' if len(coincidences) < 2 else coincidences
        return render(request, 'catalog/filters/aluminium.html', args)

    elif request.method == "GET":

        try:
            if id == -1:
                rad = AluminiumRadiator.objects.all()[0]
            else:
                rad = AluminiumRadiator.objects.get(id=id)
        except AluminiumRadiator.DoesNotExist:
            args['ex_title'] = "404 Not Found"
            args['ex_text'] = "В каталоге не найдено подходящего радиатора данной категории"
            return render(request, "mainApp/404.html", args)
        except IndexError:
            args['ex_title'] = "404 Not Found"
            args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
            return render(request, "mainApp/404.html", args)
        args['radiator'] = rad
        args['components'] = ComponentPart.objects.order_by('?')[:4]
        args['manufacturers'] = list(
            set([rad[0] for rad in AluminiumRadiator.objects.all().values_list('manufacturer__name')]))
        coincidences = find_coincidences_aluminium_similar(rad, AluminiumRadiator, request)
        args['coincidences'] = '' if len(coincidences) < 2 else coincidences
        return render(request, 'catalog/filters/aluminium.html', args)


@csrf_exempt
def bimetal_view(request, id=-1):
    args = {}
    post_data = request.POST
    args['components'] = get_components_for_see_also(4)

    if request.method == "POST" and post_data.get('parameters'):
        tuples_for_options = BimetalRadiator.objects.all().values_list('manufacturer__name', 'width',
                                                                       'depth', 'height',
                                                                       'center_distance', 'connection_type__name')
        params = json.loads(post_data.get('parameters'))
        option_id = post_data.get('optionID')
        unit = post_data.get('unit')

        args.update(get_suitable_options(params, tuples_for_options))
        args['option_id'] = option_id
        args['unit'] = unit

        return render(request, 'catalog/includes/options.html', args)

    elif request.method == "POST" and post_data.get('radiatorOptions'):
        tuples_for_radiator_search = BimetalRadiator.objects.all().values_list('manufacturer__name', 'width', 'depth',
                                                                               'height', 'center_distance',
                                                                               'connection_type__name', 'id')
        options = json.loads(post_data.get('radiatorOptions'))
        suitable_radiator = get_first_suitable_rad(options, tuples_for_radiator_search)
        if suitable_radiator:
            suitable_radiator = BimetalRadiator.objects.get(id=suitable_radiator[6])
        args['radiator'] = suitable_radiator
        args['manufacturers'] = list(
            set([rad[0] for rad in BimetalRadiator.objects.all().values_list('manufacturer__name')]))
        coincidences = find_coincidences_aluminium_similar(suitable_radiator, BimetalRadiator, request)
        args['coincidences'] = '' if len(coincidences) < 2 else coincidences
        return render(request, 'catalog/filters/bimetal.html', args)

    elif request.method == "GET":
        try:
            if id == -1:
                rad = BimetalRadiator.objects.all()[0]
            else:
                rad = BimetalRadiator.objects.get(id=id)
        except BimetalRadiator.DoesNotExist:
            args['ex_title'] = "404 Not Found"
            args['ex_text'] = "В каталоге не найдено подходящего радиатора данной категории"
            return render(request, "mainApp/404.html", args)
        except IndexError:
            args['ex_title'] = "404 Not Found"
            args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
            return render(request, "mainApp/404.html", args)
        args['radiator'] = rad
        args['manufacturers'] = list(
            set([rad[0] for rad in BimetalRadiator.objects.all().values_list('manufacturer__name')]))
        coincidences = find_coincidences_aluminium_similar(rad, BimetalRadiator, request)
        args['coincidences'] = '' if len(coincidences) < 2 else coincidences
        return render(request, 'catalog/filters/bimetal.html', args)


@csrf_exempt
def design_view(request, manufacturer_id='', id=-1):
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
        coincidences = find_coincidences_design(suitable_radiator, request)
        args['coincidences'] = '' if len(coincidences) < 2 else coincidences
        return render(request, 'catalog/filters/design.html', args)

    elif request.method == "GET":
        try:
            if id == -1:
                rad = DesignRadiator.objects.filter(manufacturer__id=manufacturer_id)[0]
            else:
                rad = DesignRadiator.objects.get(id=id)
        except DesignRadiator.DoesNotExist:
            args['ex_title'] = "404 Not Found"
            args['ex_text'] = "В каталоге не найдено подходящего радиатора данной категории"
            return render(request, "mainApp/404.html", args)
        except IndexError:
            args['ex_title'] = "404 Not Found"
            args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
            return render(request, "mainApp/404.html", args)

        args['radiator'] = rad
        args['manufacturers'] = list(
            set([rad[0] for rad in DesignRadiator.objects.all().values_list('manufacturer__name')]))
        coincidences = find_coincidences_design(rad, request)
        args['coincidences'] = '' if len(coincidences) < 2 else coincidences
        return render(request, 'catalog/filters/design.html', args)


@csrf_exempt
def steel_panel_view(request, id=-1):
    args = {}
    post_data = request.POST
    args['components'] = get_components_for_see_also(4)

    if request.method == "POST" and post_data.get('parameters'):
        tuples_for_options = SteelPanelRadiator.objects.all().values_list('manufacturer__name', 'width',
                                                                          'depth', 'height',
                                                                          'center_distance', 'connection_type__name')
        params = json.loads(post_data.get('parameters'))
        option_id = post_data.get('optionID')
        unit = post_data.get('unit')

        args.update(get_suitable_options(params, tuples_for_options))
        args['option_id'] = option_id
        args['unit'] = unit

        return render(request, 'catalog/includes/options.html', args)

    elif request.method == "POST" and post_data.get('radiatorOptions'):
        tuples_for_radiator_search = SteelPanelRadiator.objects.all().values_list('manufacturer__name',
                                                                                  'width',
                                                                                  'depth', 'height',
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
        coincidences = find_coincidences_aluminium_similar(suitable_radiator, SteelPanelRadiator, request)
        args['coincidences'] = '' if len(coincidences) < 2 else coincidences
        return render(request, 'catalog/filters/steel-panel.html', args)

    elif request.method == "GET":
        try:
            if id == -1:
                rad = SteelPanelRadiator.objects.all()[0]
            else:
                rad = SteelPanelRadiator.objects.get(id=id)

        except SteelPanelRadiator.DoesNotExist:
            args['ex_title'] = "404 Not Found"
            args['ex_text'] = "В каталоге не найдено подходящего радиатора данной категории"
            return render(request, "mainApp/404.html", args)
        except IndexError:
            args['ex_title'] = "404 Not Found"
            args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
            return render(request, "mainApp/404.html", args)
        args['radiator'] = rad
        args['manufacturers'] = list(
            set([rad[0] for rad in SteelPanelRadiator.objects.all().values_list('manufacturer__name')]))
        coincidences = find_coincidences_aluminium_similar(rad, SteelPanelRadiator, request)
        args['coincidences'] = '' if len(coincidences) < 2 else coincidences
        return render(request, 'catalog/filters/steel-panel.html', args)


@csrf_exempt
def steel_tubular_view(request, id=-1):
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
        coincidences = find_coincidences_steel_tubular(suitable_radiator, request)
        args['coincidences'] = '' if len(coincidences) < 2 else coincidences
        return render(request, 'catalog/filters/steel-tubular.html', args)


    elif request.method == "GET":
        try:
            if id == -1:
                rad = SteelTubularRadiator.objects.all()[0]
            else:
                rad = SteelTubularRadiator.objects.get(id=id)
        except SteelTubularRadiator.DoesNotExist:
            args['ex_title'] = "404 Not Found"
            args['ex_text'] = "В каталоге не найдено подходящего радиатора данной категории"
            return render(request, "mainApp/404.html", args)
        except IndexError:
            args['ex_title'] = "404 Not Found"
            args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
            return render(request, "mainApp/404.html", args)
        args['radiator'] = rad
        args['manufacturers'] = list(
            set([rad[0] for rad in SteelTubularRadiator.objects.all().values_list('manufacturer__name')]))
        coincidences = find_coincidences_steel_tubular(rad, request)
        args['coincidences'] = '' if len(coincidences) < 2 else coincidences
        return render(request, 'catalog/filters/steel-tubular.html', args)


@csrf_exempt
def steel_tubular_kzto_view(request, id=-1):
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
        coincidences = find_coincidences_steel_tubular_kzto(suitable_radiator, request)
        args['coincidences'] = '' if len(coincidences) < 2 else coincidences
        return render(request, 'catalog/filters/steel-tubular-kzto.html', args)

    elif request.method == "GET":
        try:
            if id == -1:
                rad = SteelTubularKZTORadiator.objects.all()[0]
            else:
                rad = SteelTubularKZTORadiator.objects.get(id=id)
        except SteelTubularKZTORadiator.DoesNotExist:
            args['ex_title'] = "404 Not Found"
            args['ex_text'] = "В каталоге не найдено подходящего радиатора данной категории"
            return render(request, "mainApp/404.html", args)
        except IndexError:
            args['ex_title'] = "404 Not Found"
            args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
            return render(request, "mainApp/404.html", args)
        args['radiator'] = rad
        args['manufacturers'] = list(
            set([rad[0] for rad in SteelTubularRadiator.objects.all().values_list('manufacturer__name')]))
        coincidences = find_coincidences_steel_tubular_kzto(rad, request)
        args['coincidences'] = '' if len(coincidences) < 2 else coincidences
        return render(request, 'catalog/filters/steel-tubular-kzto.html', args)


@csrf_exempt
def cost_iron_view(request, manufacturer_id='', id=-1):
    args = {}
    post_data = request.POST
    args['components'] = get_components_for_see_also(4)

    if request.method == "POST" and post_data.get('parameters'):
        tuples_for_options = CostIronRadiator.objects.all().values_list('manufacturer__name', 'width',
                                                                        'depth', 'height',
                                                                        'center_distance', 'connection_type__name')
        params = json.loads(post_data.get('parameters'))
        option_id = post_data.get('optionID')
        unit = post_data.get('unit')

        args.update(get_suitable_options(params, tuples_for_options))
        args['option_id'] = option_id
        args['unit'] = unit

        return render(request, 'catalog/includes/options.html', args)

    elif request.method == "POST" and post_data.get('radiatorOptions'):
        tuples_for_radiator_search = CostIronRadiator.objects.all().values_list('manufacturer__name', 'width',
                                                                                'depth', 'height',
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
        coincidences = find_coincidences_aluminium_similar(suitable_radiator, CostIronRadiator, request)
        args['coincidences'] = '' if len(coincidences) < 2 else coincidences
        return render(request, 'catalog/filters/cost-iron.html', args)

    elif request.method == "GET":
        try:
            if id == -1:
                rad = CostIronRadiator.objects.filter(manufacturer__id=manufacturer_id)[0]
            else:
                rad = CostIronRadiator.objects.get(id=id)

        except CostIronRadiator.DoesNotExist:
            args['ex_title'] = "404 Not Found"
            args['ex_text'] = "В каталоге не найдено подходящего радиатора данной категории"
            return render(request, "mainApp/404.html", args)
        except IndexError:
            args['ex_title'] = "404 Not Found"
            args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
            return render(request, "mainApp/404.html", args)
        args['radiator'] = rad
        args['components'] = ComponentPart.objects.order_by('?')[:4]
        args['manufacturers'] = list(
            set([rad[0] for rad in CostIronRadiator.objects.all().values_list('manufacturer__name')]))
        coincidences = find_coincidences_aluminium_similar(rad, CostIronRadiator, request)
        args['coincidences'] = '' if len(coincidences) < 2 else coincidences
        return render(request, 'catalog/filters/cost-iron.html', args)


@csrf_exempt
def floor_convector_view(request, manufacturer_id='', id=-1):
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
        coincidences = find_coincidences_floor_similar(suitable_radiator, FloorConvector, request)
        args['coincidences'] = '' if len(coincidences) < 2 else coincidences
        return render(request, 'catalog/filters/floor_convector.html', args)

    elif request.method == "GET":
        try:
            if id == -1:
                rad = FloorConvector.objects.filter(manufacturer__id=manufacturer_id)[0]
            else:
                rad = FloorConvector.objects.get(id=id)

        except FloorConvector.DoesNotExist:
            args['ex_title'] = "404 Not Found"
            args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
            return render(request, "mainApp/404.html", args)
        args['radiator'] = rad
        args['components'] = ComponentPart.objects.order_by('?')[:4]
        args['manufacturers'] = list(
            set([rad[0] for rad in FloorConvector.objects.all().values_list('manufacturer__name')]))
        coincidences = find_coincidences_floor_similar(rad, FloorConvector, request)
        args['coincidences'] = '' if len(coincidences) < 2 else coincidences
        return render(request, 'catalog/filters/floor_convector.html', args)


@csrf_exempt
def wall_convector_view(request, manufacturer_id='', id=-1):
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
        coincidences = find_coincidences_floor_similar(suitable_radiator, WallConvector, request)
        args['coincidences'] = '' if len(coincidences) < 2 else coincidences
        return render(request, 'catalog/filters/wall_convector.html', args)

    elif request.method == "GET":
        try:
            if id == -1:
                rad = WallConvector.objects.filter(manufacturer__id=manufacturer_id)[0]
            else:
                rad = WallConvector.objects.get(id=id)

        except WallConvector.DoesNotExist:
            args['ex_title'] = "404 Not Found"
            args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
            return render(request, "mainApp/404.html", args)
        args['radiator'] = rad
        args['components'] = ComponentPart.objects.order_by('?')[:4]
        args['manufacturers'] = list(
            set([rad[0] for rad in WallConvector.objects.all().values_list('manufacturer__name')]))
        coincidences = find_coincidences_floor_similar(rad, WallConvector, request)
        args['coincidences'] = '' if len(coincidences) < 2 else coincidences
        return render(request, 'catalog/filters/wall_convector.html', args)


@csrf_exempt
def recessed_convector_view(request, manufacturer_id='', id=-1):
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
            if id == -1:
                rad = RecessedConvector.objects.filter(manufacturer__id=manufacturer_id)[0]
            else:
                rad = RecessedConvector.objects.get(id=id)

        except RecessedConvector.DoesNotExist:
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
    args = {}
    if ComponentType.objects.all():
        args = {'all_categories': ComponentType.objects.all()}
    else:
        args['ex_title'] = "404 Not Found"
        args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
        return render(request, "mainApp/404.html", args)

    return render(request, 'catalog/categories_lists/components-categories.html', args)


def component_type_list_view(request, component_type_id=None):
    args = {}
    components = ComponentPart.objects.filter(type_id=component_type_id)
    if components:
        args = {'components': components}
    else:
        args['ex_title'] = "404 Not Found"
        args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
        return render(request, "mainApp/404.html", args)
    return render(request, 'catalog/lists/component-parts.html', args)


def component_page_view(request, component_type_id=None, component_id=None):
    args = {}
    if ComponentPart.objects.filter(id=component_id)[0]:
        args = {'component': ComponentPart.objects.filter(id=component_id)[0]}
    else:
        args['ex_title'] = "404 Not Found"
        args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
        return render(request, "mainApp/404.html", args)
    return render(request, "catalog/pages/component-part-page.html", args)


def design_list_view(request):
    args = {}
    if DesignRadiator.objects:
        args = get_list_information(radiators_count=3, radiators_class=DesignRadiator, radiator_type_id=1)
    else:
        args['ex_title'] = "404 Not Found"
        args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
        return render(request, "mainApp/404.html", args)
    return render(request, 'catalog/lists/design.html', args)


def cost_iron_list_view(request):
    args = {}
    if DesignRadiator.objects:
        args = get_list_information(radiators_count=3, radiators_class=CostIronRadiator, radiator_type_id=2)
    else:
        args['ex_title'] = "404 Not Found"
        args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
        return render(request, "mainApp/404.html", args)
    return render(request, 'catalog/lists/cost-iron.html', args)


def convector_categories_view(request):
    return render(request, 'catalog/categories_lists/convector.html', {})


def floor_convector_list_view(request):
    args = {}
    if DesignRadiator.objects:
        args = get_list_information(radiators_count=3, radiators_class=FloorConvector, radiator_type_id=4)
    else:
        args['ex_title'] = "404 Not Found"
        args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
        return render(request, "mainApp/404.html", args)

    return render(request, 'catalog/lists/floor_convector.html', args)


def wall_convector_list_view(request):
    args = {}
    if DesignRadiator.objects:
        args = get_list_information(radiators_count=3, radiators_class=WallConvector, radiator_type_id=5)
    else:
        args['ex_title'] = "404 Not Found"
        args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
        return render(request, "mainApp/404.html", args)

    return render(request, 'catalog/lists/wall_convector.html', args)


def recessed_convector_list_view(request):
    args = {}
    if DesignRadiator.objects:
        args = get_list_information(radiators_count=3, radiators_class=RecessedConvector, radiator_type_id=3)
    else:
        args['ex_title'] = "404 Not Found"
        args['ex_text'] = "В каталоге не найдено ни одного радиатора данной категории"
        return render(request, "mainApp/404.html", args)

    return render(request, 'catalog/lists/recessed_convector.html', args)


@csrf_exempt
def search_view(request):
    if request.method == "POST":
        args = {}
        search_string = request.POST.get('search_string')
        if search_in_categories(search_string):
            args.update(search_in_categories(search_string))
        args.update(search_in_all_list(search_string))
        args.update(search_in_components(search_string))

        return render(request, 'mainApp/search.html', args)
