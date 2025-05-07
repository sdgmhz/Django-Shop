import re
from django.core.exceptions import ValidationError


def validate_iranian_mobile(value):
    """
    Validates Iranian mobile numbers in the format +989xxxxxxxxx
    """
    pattern = r"^\+989\d{9}$"
    if not re.match(pattern, value):
        raise ValidationError("Phone number must be in format +989xxxxxxxxx")


def validate_persian_name(value):
    """
    Validates Persian names (only Persian letters and spaces allowed)
    """
    pattern = r"^[آ-یءئإأاچژپگکی‌ ]+$"
    if not re.match(pattern, value):
        raise ValidationError("Name must contain only Persian letters and spaces")
