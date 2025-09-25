import logging
import re
try:
    from email_validator import validate_email, EmailNotValidError except ImportError:
    validate_email = None

logger = logging.getLongger(__name__)

def validate_email_address(email: str) -> tuple[bool, str]:
    if not email:
        return False, "Email address cannot be empty"

    email = email.strip().lower()

    if validate_email:
        try:
            validate_email(email, check_deliverability=False)
            return True, "Valid email address"
        except EmailNotValidError as e:
            logger.error(f"Email validation failed for {email}: {str(e)}")
            return False, f"Invalid email address: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error during email validation for {email}: {str(e)}")
            return False, "An unexpected error occured during email validation"
    
    else:
        pattern = r'^[a-zA-Z0-9.%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        try:
            if re.match(pattern, email):
                return True, "Valid email address (regex validation)"
            else:
                logger.warning(f"Regex-based email validation failed for {email}")
                return False, "Invalid email address format"
        except Exception as e:
            logger.error(f"Regex validation error for {email}: {str(e)}")
            return False, "An error occured during regex-based email validation"