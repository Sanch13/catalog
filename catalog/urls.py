from django.urls import path, include

from catalog.views import catalog

app_name = "catalog"


urlpatterns = [
    path('about/', catalog.about_miran, name="about_miran"),
    path('contact/', catalog.contact_me, name="contact_me"),
    path('', catalog.get_catalog, name="catalog"),
    path('<slug:category_slug>/', catalog.get_category, name="category"),
    path('<slug:category_slug>/<slug:series_slug>/<slug:product_slug>/', catalog.get_product_detail,
         name="product_detail"),
    path('<slug:category_slug>/<slug:product_slug>/', catalog.product_detail_no_series,
         name="product_detail_no_series"),
    path('new/<slug:product_slug>/', catalog.product_detail_no_series,
         name="new_products"),
    path('send_data_to_email', catalog.send_data_to_email, name="send_data_to_email"),
    path('send_data_form_price_to_email', catalog.send_data_form_price_to_email, name="send_data_form_price_to_email"),
    path('send_data_to_email_from_supplier',
         catalog.send_data_to_email_from_supplier,
         name="send_data_to_email_from_supplier"),
    path('get_size_list_files', catalog.get_size_list_pdf_files, name="get_size_list_files"),
    path('get_size_new_products', catalog.get_size_new_products, name="get_size_new_products"),

]
