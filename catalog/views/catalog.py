from django.shortcuts import render, redirect, get_object_or_404

from catalog.models.catalog import Category
from catalog.models.cap import Cap


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
    print(category.name)
    if category.name == 'Флаконы':
        # flakons = Flakon.objects.filter(category=category)
        # context = {
        #     'flakons': flakons
        # }
        return render(request, 'catalog/flakony.html', {})
    elif category.name == 'Баночки':
        # jars = Jar.objects.filter(category=category)
        # context = {
        #     'jars': jars
        # }
        return render(request, 'catalog/jars.html', {})
    elif category.name == 'Колпачки':
        caps = Cap.objects.filter(category=category)
        return render(request, 'catalog/caps.html', {'caps': caps})
    return render(request, 'catalog/category.html', {'category': category})




# def get_product_detail(request, category_slug, series_slug=None, product_slug=None):
#     if series_slug:
#         product = get_object_or_404(Product,
#                                     slug=product_slug, series__slug=series_slug, category__slug=category_slug)
    # else:
    #     product = get_object_or_404(Product, slug=product_slug, category__slug=category_slug)
    # context = {
    #     "product": product,
    # }
    # return render(request=request,
    #               template_name="catalog/product_detail.html",
    #               context=context)


# def get_series_detail(request, category_slug, series_slug):
#     category = get_object_or_404(Series, slug=series_slug, category__slug=category_slug)
#     products = series.products.all()
#     context = {
#         "series": series,
#         "products": products,
#     }
#     return render(request=request,
#                   template_name="catalog/series_detail.html",
#                   context=context)
