from rest_framework.serializers import ValidationError

def validate_component_code(code):
    if not code:
        raise ValidationError('You must specify a code')

    code = str(code)
    if len(code) != 4 or not code.isdigit():
        raise ValidationError('Invalid code')
    return code



