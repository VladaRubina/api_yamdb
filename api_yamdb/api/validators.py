import re

from django.forms import ValidationError


def validate_username(value):
    pattern = r'^[\w.@+-]+\Z'
    if not re.match(pattern, value):
        raise ValidationError('Недопустимые символы в никнейме')
    if 'me' == value:
        raise ValidationError('Недопустимое имя')
