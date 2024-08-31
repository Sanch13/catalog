from email.message import EmailMessage
import smtplib
import ssl

from django.template.loader import get_template

from celery import shared_task

from catalog.models import EmailLog
from catalog.utils import (
    file_exists_in_directory,
    create_pdf_from_data,
    merge_pdfs_to_stream, send_data_to_client, send_data_to_marketing
)
from settings import settings


@shared_task()
def send_email_list_products(list_params, data):
    list_of_path_pdf = [params['path_to_pdf'] for params in list_params]
    products = [params['name'] for params in list_params]
    file_stream = merge_pdfs_to_stream(pdf_paths=list_of_path_pdf)
    try:
        send_data_to_client(list_params, data, file_stream)
        status = "Success"
    except Exception as e:
        status = f"Failed: {str(e)}"

    send_data_to_marketing(data, status, products)

    EmailLog.objects.create(
        name=data["name"],
        company=data["company"],
        phone_number=data["phone_number"],
        email=data["email"],
        comment=data["comment"],
        category=data["category"],
        place=data["place"],
        status=status,
        products=products,
        lead_qualification=EmailLog.LeadQualification.CUSTOMER
    )



