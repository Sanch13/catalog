from celery import shared_task
from catalog.models import EmailLog
from catalog.utils import (
    merge_pdfs_to_stream,
    send_data_to_client,
    send_data_to_sale,
    send_admin_email,
    send_email_to_department,
    save_data_to_db_with_status, get_params_from_category
)


@shared_task()
def send_email_list_products(list_params, user_data):
    if not list_params:
        return

    list_of_path_pdf = [params['path_to_pdf'] for params in list_params]
    file_stream = merge_pdfs_to_stream(pdf_paths=list_of_path_pdf)
    user_data["products"] = [params['name'] for params in list_params]

    try:
        send_data_to_client(list_params, user_data, file_stream)
        status = "Клиент запросил информацию из каталога.\nПисьмо клиенту доставлено"
        user_data["status"] = status
        try:
            save_data_to_db_with_status(user_data,
                                        lead_qualification=EmailLog.LeadQualification.CUSTOMER)
            send_data_to_sale(user_data)
        except Exception as e:
            send_admin_email(text_body=f"An unexpected error occurred: {e}")

    except Exception as e:
        status = f"Failed: {str(e)}"
        user_data["status"] = status
        send_admin_email(text_body=f"An unexpected error occurred: {e}")
        save_data_to_db_with_status(user_data,
                                    lead_qualification=EmailLog.LeadQualification.CUSTOMER)


@shared_task()
def send_email_from_contact_customer(user_data):
    user_data["status"] = "покупатель из свяжитесь со мной"
    try:
        save_data_to_db_with_status(user_data,
                                    lead_qualification=EmailLog.LeadQualification.CUSTOMER)
        send_data_to_sale(user_data)
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


@shared_task()
def send_data_form_price_to_sale(user_data):
    list_params = get_params_from_category(user_data)

    if user_data["form"] == "price":
        user_data["status"] = "Запрос цены на выбранную продукцию"

    user_data["products"] = [params['name'] for params in list_params]
    try:
        send_data_to_sale(user_data)
        save_data_to_db_with_status(user_data,
                                    lead_qualification=EmailLog.LeadQualification.CUSTOMER)
    except Exception as e:
        status = f"Failed: {str(e)}"
        user_data["status"] = status
        send_admin_email(text_body=user_data)
        save_data_to_db_with_status(user_data,
                                    lead_qualification=EmailLog.LeadQualification.CUSTOMER)
