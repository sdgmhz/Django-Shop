import re
from django.core.exceptions import ValidationError


def validate_discount_percent(value):
    pattern = r"^09\d{9}$"
    if not re.match(pattern, value):
        raise ValidationError("Enter an integer number between 0 and 100")
