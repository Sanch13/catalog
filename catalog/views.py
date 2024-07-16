from django.shortcuts import render

from catalog.models import Category, Cap


def main(request):
    return redirect(to="catalog:home")


def get_catalog(request):
    categories = Category.objects.all()
    context = {
        "categories": categories
    }
    return render(request=request,
                  template_name="catalog/catalog.html",
                  context=context)
