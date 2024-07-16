from django.urls import path, include

from .views import get_catalog, category_detail

app_name = "catalog"


urlpatterns = [
    path('', get_catalog, name="home"),
    path('<slug:category_slug>/', category_detail, name="category"),
]
