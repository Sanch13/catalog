from django.db.models import OuterRef, Subquery
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from catalog.models import Jar, Series, Cap, Category, Bottle, CapFile, JarFile, BottleFile


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

        paginator = Paginator(series, 4)
        page_number = request.GET.get('page', 1)
        series = paginator.page(page_number)
        context = {
            'series': series
        }
        return render(request=request,
                      template_name='catalog/series.html',
                      context=context)

    elif category.name == 'Баночки':
        jars = Jar.objects.filter(category=category)

        paginator = Paginator(jars, 4)
        page_number = request.GET.get('page', 1)
        jars = paginator.page(page_number)
        context = {
            'jars': jars
        }
        return render(request=request,
                      template_name='catalog/jars.html',
                      context=context)

    elif category.name == 'Колпачки':
        caps = Cap.objects.filter(category=category)

        paginator = Paginator(caps, 4)
        page_number = request.GET.get('page', 1)
        caps = paginator.page(page_number)
        context = {
            'caps': caps
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
            image=Subquery(cap_image_subquery)).values('name', 'slug', 'status', 'ratings',
                                                       'category__slug', 'image')
        jars = Jar.objects.filter(status='Новинка').annotate(
            image=Subquery(jar_image_subquery)).values('name', 'slug', 'status', 'ratings',
                                                       'category__slug', 'image')
        bottles = Bottle.objects.filter(status='Новинка').annotate(
            image=Subquery(bottle_image_subquery)).values('name', 'slug', 'status', 'ratings',
                                                          'category__slug', 'image')

        all_new_products = caps.union(jars, bottles).order_by('-ratings')
        paginator = Paginator(all_new_products, 4)
        page_number = request.GET.get('page', 1)
        all_new_products = paginator.page(page_number)
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
