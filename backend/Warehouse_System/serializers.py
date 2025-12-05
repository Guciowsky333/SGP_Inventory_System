from rest_framework import serializers
from Warehouse_System.models import Component, Localization

class ComponentSerializer(serializers.ModelSerializer):
    localization = serializers.SlugRelatedField(
        queryset=Localization.objects.all(),
        slug_field='localization_name'
    )
    class Meta:
        model = Component
        fields = ['localization', 'code', 'quantity']
    def validate_code(self, value):
        code = str(value)
        if len(code) != 4:
            raise serializers.ValidationError('code must be 4 characters')
        if not code.isdigit():
            raise serializers.ValidationError('code must be an integer')
        return code

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError('quantity must be greater than 0')
        return value


