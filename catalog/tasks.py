from celery import shared_task
from catalog.models import EmailLog
from catalog.utils import (
    merge_pdfs_to_stream,
    send_data_to_client,
    send_data_to_marketing,
    send_admin_email,
    send_email_to_department
)


@shared_task()
def send_email_list_products(list_params, data):
    list_of_path_pdf = [params['path_to_pdf'] for params in list_params]
    products = [params['name'] for params in list_params]
    file_stream = merge_pdfs_to_stream(pdf_paths=list_of_path_pdf)

    try:
        send_data_to_client(list_params, data, file_stream)
        status = "Success"
        try:
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
            send_data_to_marketing(data, status, products)
        except Exception as e:
            send_admin_email(text_body=f"An unexpected error occurred: {e}")

    except Exception as e:
        status = f"Failed: {str(e)}"
        send_admin_email(text_body=status)
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


@shared_task()
def send_email_from_contact_customer(data):
    status = "Покупатель из <Свяжитесь со  мной> "
    try:
        EmailLog.objects.create(
            name=data["name"],
            company=data["company"],
            phone_number=data["phone_number"],
            email=data["email"],
            comment=data["comment"],
            category='no category',
            place=data["place"],
            status=status,
            products=[],
            lead_qualification=EmailLog.LeadQualification.CUSTOMER,
        )
        send_data_to_marketing(data, status=status, products=None)
    except Exception as e:
        send_admin_email(text_body=f"An unexpected error occurred: {e}")


@shared_task()
def send_department_email(data):
    try:
        send_email_to_department(data=data)
        try:
            EmailLog.objects.create(
                name=data["name"],
                company=data["company"],
                phone_number='',
                email=data["email"],
                comment=data["comment"],
                category=data["department"],
                place='supplier',
                status="Success",
                products=[],
                lead_qualification=EmailLog.LeadQualification.SUPPLIER
            )
        except Exception as e:
            send_admin_email(text_body=f"An unexpected error occurred: {e}")

    except Exception as e:
        send_admin_email(text_body=f"An unexpected error occurred: {e}")
