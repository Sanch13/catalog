from django.db.models import OuterRef, Subquery, Value
from django.db.models.functions import Coalesce
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse

from catalog.forms import CapFilterForm, JarFilterForm, BottlesFilterForm, SendDataToEmail
from catalog.models import Jar, Series, Cap, Category, Bottle, CapFile, JarFile, BottleFile
from catalog.tasks import send_email
from catalog.utils import get_jar_data_from_db, create_pdf_from_data


# from ..utils import get_objects_from_paginator


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
        form = BottlesFilterForm(request.GET or None)
        series = Series.objects.filter(category=category)

        if form.is_valid():
            throat_standard = form.cleaned_data.get('throat_standard')
            volume = form.cleaned_data.get("volume")
            status_decoration = form.cleaned_data.get("status_decoration")
            surface = form.cleaned_data.get("surface")
            # print(f'volume: {volume} \nsurface: {surface} \ndecoration: \
            # {status_decoration}\nthroat_standard: {throat_standard}')
            if throat_standard:
                series = series.filter(bottle__throat_standard__in=throat_standard).distinct()
            if volume:
                series = series.filter(bottle__volume__range=volume).distinct()
            if status_decoration:
                series = series.filter(bottle__status_decoration=status_decoration).distinct()
            if surface:
                series = series.filter(bottle__surface__in=surface).distinct()

        context = {
            'series': series,
            'form': form
        }
        return render(request=request,
                      template_name='catalog/series.html',
                      context=context)

    elif category.name == 'Баночки':
        form = JarFilterForm(request.GET or None)
        jars = Jar.objects.filter(category=category)

        if form.is_valid():
            volume = form.cleaned_data.get('volume')
            surface = form.cleaned_data.get('surface')
            status_decoration = form.cleaned_data.get('status_decoration')
            # print(f'volume:{volume}  | surface:{surface}  | decoration:{status_decoration}')
            if volume:
                jars = jars.filter(volume__range=volume)
            if surface:
                jars = jars.filter(surface__in=surface)
            if status_decoration:
                jars = jars.filter(status_decoration=status_decoration)

        context = {
            'jars': jars,
            'form': form,
        }
        return render(request=request,
                      template_name='catalog/jars.html',
                      context=context)

    elif category.name == 'Колпачки':
        form = CapFilterForm(request.GET or None)
        caps = Cap.objects.filter(category=category)

        if form.is_valid():
            throat_standard = form.cleaned_data.get('throat_standard')
            type_of_closure = form.cleaned_data.get('type_of_closure')
            surface = form.cleaned_data.get('surface')
            # print(throat_standard, type_of_closure, surface)
            if throat_standard:
                caps = caps.filter(throat_standard__in=throat_standard)
            if type_of_closure:
                caps = caps.filter(type_of_closure__in=type_of_closure)
            if surface:
                caps = caps.filter(surface__in=surface)

        context = {
            'caps': caps,
            'form': form,
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
    volume = request.GET.get('volume')

    if volume:
        bottle = get_object_or_404(Bottle,
                                   category__slug=category_slug,
                                   series__slug=series_slug,
                                   volume=volume,
                                   slug=product_slug)
    else:
        bottle = get_object_or_404(Bottle,
                                   category__slug=category_slug,
                                   series__slug=series_slug,
                                   slug=product_slug)

    bottles = Bottle.objects.filter(series__slug=series_slug)
    context = {
        "bottle": bottle,
        "bottles": bottles,
    }
    return render(request=request,
                  template_name="catalog/bottle_detail.html",
                  context=context)


def product_detail_no_series(request, category_slug, product_slug):
    if category_slug == "jars":
        form = SendDataToEmail()
        jar = get_object_or_404(Jar,
                                category__slug=category_slug,
                                slug=product_slug)
        context = {
            "form": form,
            "jar": jar
        }
        return render(request=request,
                      template_name="catalog/jar_detail.html",
                      context=context)

    elif category_slug == 'caps':
        cap = get_object_or_404(Cap,
                                category__slug=category_slug,
                                slug=product_slug)
        context = {
            "cap": cap
        }
        return render(request=request,
                      template_name='catalog/cap_detail.html',
                      context=context)

    elif category_slug == 'bottles':
        bottle = get_object_or_404(Bottle,
                                   category__slug=category_slug,
                                   slug=product_slug)
        context = {
            "bottle": bottle
        }
        return render(request=request,
                      template_name='catalog/bottle_detail.html',
                      context=context)


def send_data_to_email(request):
    if request.method == 'POST':
        form = SendDataToEmail(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print("Form is valid")
            print(cd)
            name = cd["name"]
            email = cd["email"]

            ids = request.POST.get('ids')
            params = get_jar_data_from_db(id_item=ids)

            send_email.delay(params, email, name)

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
