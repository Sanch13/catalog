from django.urls import path, include

from .views import get_catalog

app_name = "catalog"


urlpatterns = [
    path('', get_catalog, name="catalog"),
]
