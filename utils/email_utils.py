import logging
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
from utils.validation_utils import validate_email_address

logger = logging.getLogger(__name__)

def send_order_Confirmation_email(order_id: int, customer_email: str, customer_name: str, order_details: dict) -> tuple[bool, str]:
    is_valid_email, email_message = validate_email_address(customer_email)
    if not is_valid_email:
        logger.error(f"Invalid email for order {order_id}: {email_message}")
        return False, email_message
    try:
        subject = f"Order Confirmation - Order #{order_id}"
        context = {
            'customer_name': customer_name,
            'order_id': order_id,
            'order_details': order_details,
            'total_amount': order_details.get('total_amount', 0.00),
            'items': order_details.get('items', []),
        }

        message = render_to_string('emails/order_confirmation.html', context)

        send_mail(
            subject=subject,
            message='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[customer_email],
            html_message=message,
            fail_silently=False,
        )
        logger.info(f"Order confirmation email sent successfully for order {order_id} to {customer_email}")
        return True, "Order confirmation email sent successfully"
    
    except ValidationError as e:
        logger.error(f"Validation error sending error email for order {order_id}: {str(e)}")
        return False, f"Failed to send email: Invalid email configuration"
    except Exception as e:
        logger.error(f"Error sending email for order {order_id} to {customer_email}: {str(e)}")
        return False, f"Failed to send email: {str(e)}"
