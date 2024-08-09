from django.db.models import OuterRef, Subquery, Value
from django.db.models.functions import Coalesce
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from catalog.forms import CapFilterForm
from catalog.models import Jar, Series, Cap, Category, Bottle, CapFile, JarFile, BottleFile


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
        series = Series.objects.filter(category=category)

        # series = get_objects_from_paginator(request, per_page=4, model_objects_list=series)
        context = {
            'series': series
        }
        return render(request=request,
                      template_name='catalog/series.html',
                      context=context)

    elif category.name == 'Баночки':
        jars = Jar.objects.filter(category=category)

        # jars = get_objects_from_paginator(request, per_page=4, model_objects_list=jars)
        context = {
            'jars': jars
        }
        return render(request=request,
                      template_name='catalog/jars.html',
                      context=context)

    elif category.name == 'Колпачки':
        form = CapFilterForm(request.GET or None)
        caps = Cap.objects.filter(category=category)

        # types_of_closure = [choice[0] for choice in Cap.TypeOfClosure.choices]
        # throat_standards = [choice[0] for choice in Cap.ThroatStandard.choices]

        if 'clear_filter' in request.GET:
            print('clear_filter')
            return redirect(reverse(viewname='catalog:category', args=[]))

        if form.is_valid():
            throat_standard = form.cleaned_data.get('throat_standard')
            type_of_closure = form.cleaned_data.get('type_of_closure')
            surface = form.cleaned_data.get('surface')
            print(throat_standard, type_of_closure, surface)
            if throat_standard:
                caps = caps.filter(throat_standard__in=throat_standard)
            if type_of_closure:
                caps = caps.filter(type_of_closure__in=type_of_closure)
            if surface:
                caps = caps.filter(surface__in=surface)

        context = {
            'caps': caps,
            'form': form,
            # 'types_of_closure': types_of_closure,
            # 'throat_standards': throat_standards
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
        # all_new_products = get_objects_from_paginator(request,
        #                                               per_page=4,
        #                                               model_objects_list=all_new_products)
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
        jar = get_object_or_404(Jar,
                                category__slug=category_slug,
                                slug=product_slug)
        context = {
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
