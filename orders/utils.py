import secrets
from django.db import IntegrityError
from .models import Coupon
import string

def generate_coupon_code(length=10):
    if length < 1:
        raise ValueError("Coupon code length must be at least 1")
    characters = string.ascii_uppercase + string.digits

    max_attempts = 100

    for _ in range(max_attempts):
        code = ''.join(secrets.choice(characters) for _ in range(length))

        try:
            if not Coupon.objects.filter(code=code).exists():
                return code
        except Exception as e:
            raise RuntimeError(f"Error checking coupon code uniqueness: {str(e)}")
    raise RuntimeError("Unable to generate a unique coupon code after maximum attempts")
    