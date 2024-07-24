from django.urls import path, include

from catalog.views.catalog import get_catalog, get_category, get_product_detail

app_name = "catalog"


urlpatterns = [
    path('', get_catalog, name="catalog"),
    path('<slug:category_slug>/', get_category, name="category"),
    # path('<slug:category_slug>/<slug:series_slug>/', get_series_detail, name="series_detail"),
    # path('<slug:category_slug>/<slug:series_slug>/<slug:product_slug>/', get_product_detail,
    #      name="product_detail"),
    path('<slug:category_slug>/<slug:product_slug>/', get_product_detail,
         name="product_detail_no_series"),
]
