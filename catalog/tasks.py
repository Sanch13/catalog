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
    products = [params['name'] for params in list_params]
    user_data["products"] = products
    file_stream = merge_pdfs_to_stream(pdf_paths=list_of_path_pdf)
    print(user_data)

    try:
        send_data_to_client(list_params, user_data, file_stream)
        status = "Success"
        try:
            save_data_to_db_with_status(user_data,
                                        status=status,
                                        lead_qualification=EmailLog.LeadQualification.CUSTOMER
                                        )
            send_data_to_sale(user_data, status)
        except Exception as e:
            send_admin_email(text_body=f"An unexpected error occurred: {e}")

    except Exception as e:
        status = f"Failed: {str(e)}"
        send_admin_email(text_body=status)
        save_data_to_db_with_status(user_data,
                                    status=status,
                                    lead_qualification=EmailLog.LeadQualification.CUSTOMER
                                    )


@shared_task()
def send_email_from_contact_customer(data):
    status = "Покупатель из <Свяжитесь со  мной> "
    try:
        # save_data_to_db_with_status(user_data,
        #                             status=status,
        #                             lead_qualification=EmailLog.LeadQualification.CUSTOMER
        #                             )
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
        send_data_to_sale(data, status=status, products=None)
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
    list_params = get_params_from_category(
        category=user_data["category"],
        ids=user_data["ids"],
    )
    user_data["products"] = [params['name'] for params in list_params]
    status = "Success"
    try:
        send_data_to_sale(user_data, status)
        save_data_to_db_with_status(user_data,
                                    status=status,
                                    lead_qualification=EmailLog.LeadQualification.CUSTOMER
                                    )
    except Exception as e:
        status = f"Failed: {str(e)}"
        send_admin_email(text_body=status)
        save_data_to_db_with_status(user_data,
                                    status=status,
                                    lead_qualification=EmailLog.LeadQualification.CUSTOMER
                                    )
