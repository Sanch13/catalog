import json
from pathlib import Path

from django.db.models import OuterRef, Subquery, Value, Q
from django.db.models.functions import Coalesce
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from catalog.forms import CapFilterForm, JarFilterForm, BottlesFilterForm, SendDataToEmail, \
    SendDataFromSupplierToEmail
from catalog.models import Jar, Series, Cap, Category, Bottle, CapFile, JarFile, BottleFile
from catalog.tasks import send_email_list_products, send_email_from_contact_customer
from catalog.utils import (
    create_pdf_from_data,
    file_exists_in_directory,
    get_formatted_file_size,
    convert_to_numbers,
    get_list_params_jars_from_db,
    get_query_for_request_to_db,
    get_list_params_caps_from_db,
    get_list_params_bottles_from_db
)


def home(request):
    return render(request=request,
                  template_name='catalog/home.html')


def get_catalog(request):
    categories = Category.objects.all()
    context = {
        "categories": categories
    }
    return render(request=request,
                  template_name="catalog/catalog.html",
                  context=context)


def get_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    if category.name == 'Флаконы':
        form_filter = BottlesFilterForm(request.GET or None)
        form_data_to_email = SendDataToEmail()
        series = Series.objects.filter(category=category)

        if form_filter.is_valid():
            cd = form_filter.cleaned_data
            throat_standard = cd.get('throat_standard')
            volumes = cd.get("volume")
            status_decoration = cd.get("status_decoration")
            surface = cd.get("surface")
            shape = cd.get("shape")

            if volumes:
                query = Q()
                for start, end in volumes:
                    query |= Q(bottle__volume__range=(start, end))

                series = series.filter(query).distinct()
            if throat_standard:
                series = series.filter(bottle__throat_standard__in=throat_standard).distinct()
            if status_decoration:
                series = series.filter(bottle__status_decoration=status_decoration).distinct()
            if surface:
                series = series.filter(bottle__surface__in=surface).distinct()
            if shape:
                series = series.filter(bottle__shape__in=shape).distinct()

        context = {
            'series': series,
            'form_filter': form_filter,
            'form_data_to_email': form_data_to_email,
        }
        return render(request=request,
                      template_name='catalog/series.html',
                      context=context)

    elif category.name == 'Баночки':
        form_filter = JarFilterForm(request.GET or None)
        form_data_to_email = SendDataToEmail()
        jars = Jar.objects.filter(category=category)

        if form_filter.is_valid():
            cd = form_filter.cleaned_data
            volumes = cd.get('volume')
            surface = cd.get('surface')
            status_decoration = cd.get('status_decoration')

            if volumes:
                query = get_query_for_request_to_db(list_volumes=volumes)
                jars = jars.filter(query)
            if surface:
                jars = jars.filter(surface__in=surface)
            if status_decoration:
                jars = jars.filter(status_decoration=status_decoration)

        context = {
            'jars': jars,
            'form_filter': form_filter,
            'form_data_to_email': form_data_to_email,
        }
        return render(request=request,
                      template_name='catalog/jars.html',
                      context=context)

    elif category.name == 'Колпачки':
        form_filter = CapFilterForm(request.GET or None)
        caps = Cap.objects.filter(category=category)
        form_data_to_email = SendDataToEmail()

        if form_filter.is_valid():
            cd = form_filter.cleaned_data
            throat_standard = cd.get('throat_standard')
            type_of_closure = cd.get('type_of_closure')
            surface = cd.get('surface')
            if throat_standard:
                caps = caps.filter(throat_standard__in=throat_standard)
            if type_of_closure:
                caps = caps.filter(type_of_closure__in=type_of_closure)
            if surface:
                caps = caps.filter(surface__in=surface)

        context = {
            'caps': caps,
            'form_filter': form_filter,
            'form_data_to_email': form_data_to_email,
        }
        return render(request=request,
                      template_name='catalog/caps.html',
                      context=context)

    elif category.name == 'Новинки':
        cap_image_subquery = CapFile.objects.filter(cap=OuterRef('pk')).values('file')[:1]
        jar_image_subquery = JarFile.objects.filter(jar=OuterRef('pk')).values('file')[:1]
        bottle_image_subquery = BottleFile.objects.filter(
            bottle=OuterRef('pk')).values('file')[:1]

        caps = Cap.objects.filter(status='Новинка').annotate(
            image=Subquery(cap_image_subquery),
            series_slug=Value('')
        ).values('name', 'slug', 'status', 'ratings', 'series_slug', 'category__slug', 'image')

        jars = Jar.objects.filter(status='Новинка').annotate(
            image=Subquery(jar_image_subquery),
            series_slug=Value('')
        ).values('name', 'slug', 'status', 'ratings', 'series_slug', 'category__slug', 'image')

        bottles = Bottle.objects.filter(status='Новинка').annotate(
            image=Subquery(bottle_image_subquery),
            series_slug=Coalesce('series__slug', Value(''))
        ).values('name', 'slug', 'status', 'ratings', 'series_slug', 'category__slug', 'image')

        all_new_products = caps.union(jars, bottles).order_by('-ratings')
        context = {
            'new_products': all_new_products
        }
        return render(request=request,
                      template_name='catalog/new_products.html',
                      context=context)


def get_product_detail(request, category_slug, series_slug=None, product_slug=None):
    """For bottles"""
    form_data_to_email = SendDataToEmail()
    bottle = get_object_or_404(Bottle,
                               category__slug=category_slug,
                               series__slug=series_slug,
                               slug=product_slug)
    bottles = Bottle.objects.filter(series__slug=series_slug)

    context = {
        "bottle": bottle,
        "bottles": bottles,
        "form_data_to_email": form_data_to_email,

    }
    return render(request=request,
                  template_name="catalog/bottle_detail.html",
                  context=context)


def product_detail_no_series(request, category_slug, product_slug):
    """For jars and caps"""
    if category_slug == "jars":
        form_data_to_email = SendDataToEmail()
        jar = get_object_or_404(Jar,
                                category__slug=category_slug,
                                slug=product_slug)
        context = {
            "form_data_to_email": form_data_to_email,
            "jar": jar,

        }
        return render(request=request,
                      template_name="catalog/jar_detail.html",
                      context=context)

    elif category_slug == 'caps':
        form_data_to_email = SendDataToEmail()
        cap = get_object_or_404(Cap,
                                category__slug=category_slug,
                                slug=product_slug)
        context = {
            "cap": cap,
            "form_data_to_email": form_data_to_email,
        }
        return render(request=request,
                      template_name='catalog/cap_detail.html',
                      context=context)


def send_data_to_email(request):
    print('send_data_to_email', request.POST)
    if request.method == 'POST':
        form = SendDataToEmail(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            category = request.POST.get('category', [])
            place = request.POST.get('place', [])
            user_data = {
                'name': cd['name'],
                'company': cd['company'],
                'phone_number': cd['phone_number'],
                'email': cd['email'],
                'comment': cd['comment'],
                'category': category,
                'place': place,
            }
            print("work")
            if place != 'contact':
                ids = convert_to_numbers(json.loads(request.POST.get('ids', [])))
                list_params = []
                if category == 'jar':
                    list_params = get_list_params_jars_from_db(ids)
                if category == 'cap':
                    list_params = get_list_params_caps_from_db(ids)
                if category in ('bottle', 'series'):
                    list_params = get_list_params_bottles_from_db(ids, category)

                send_email_list_products.delay(list_params=list_params, data=user_data)
                return JsonResponse({'success': True})
            else:
                send_email_from_contact_customer.delay(data=user_data)
                print("send email")
                return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


def get_size_list_pdf_files(request):
    if request.method == 'POST':
        ids = convert_to_numbers(json.loads(request.POST.get('ids', [])))
        category = request.POST.get("category")
        print(category)
        list_params = []
        if category == 'jar':
            list_params = get_list_params_jars_from_db(ids)
        if category == 'cap':
            list_params = get_list_params_caps_from_db(ids)
        if category in ('bottle', 'series'):
            list_params = get_list_params_bottles_from_db(ids, category)

        all_size = 0
        for params in list_params:
            pdf_file_path = params['path_to_pdf']
            if not file_exists_in_directory(pdf_file_path):
                pdf_file_path = create_pdf_from_data(params=params, category=category)

            size = Path(pdf_file_path).stat().st_size
            all_size += size

        file_size = get_formatted_file_size(size_bytes=all_size)
        return JsonResponse({'success': True, 'file_size': file_size})


def about_miran(request):
    return render(request=request,
                  template_name="catalog/about_miran.html")


def contact_me(request):
    form_data_to_email = SendDataToEmail()
    form_data_to_email_supplier = SendDataFromSupplierToEmail()
    context = {
        'form_data_to_email': form_data_to_email,
        'form_data_to_email_supplier': form_data_to_email_supplier,
    }
    return render(request=request,
                  template_name="catalog/contact_me.html",
                  context=context)
