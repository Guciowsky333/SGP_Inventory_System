from Warehouse_System.models import Component, Localization
from django.db import transaction
from django.db.models import Sum
from rest_framework.exceptions import ValidationError, NotFound
from Warehouse_System.validations import validate_component_code
from rest_framework.views import Response
from rest_framework import status


# =========================================================================================================== #

def process_component_placement(localization, code, quantity):

    #all necessary data
    limit_quantity_in_localization = 28
    limit_code_in_localization = 2

    with transaction.atomic():

        #Bloc localization to prevent race condition
        localization = Localization.objects.select_for_update().get(pk=localization.id)

        components = localization.components.all()

        total_quantity = localization.components.aggregate(Sum('quantity'))['quantity__sum'] or 0

        count_components = localization.components.count()

        existing_component = components.filter(code=code).first()

        #if your component is already on localization we add our quantity if total quantity after adding is equal to or less than 28
        if existing_component:
            if total_quantity + quantity <= limit_quantity_in_localization :
                existing_component.quantity += quantity
                existing_component.save()
                #Flase because we didit create new component
                return False
            else:
                raise ValidationError({'message':f'In localization {localization.localization_name}'
                                                 f' is already {total_quantity} quantity so you '
                                                 f'cant add {quantity} to it max is {limit_quantity_in_localization}'})


        if count_components == limit_code_in_localization:
            raise ValidationError({'message':f'In localization {localization.localization_name} '
                                             f'is already {count_components} components so you cant add one more '
                                             f'max components of one localization is {limit_code_in_localization}'})


        if total_quantity + quantity > limit_quantity_in_localization:
            raise ValidationError({'message':f'In localization {localization.localization_name}'
                                                 f' is already {total_quantity} quantity so you '
                                                 f'cant add {quantity} to it max is {limit_quantity_in_localization}'})

        Component.objects.create(
            localization=localization,
            code=code,
            quantity=quantity
        )

        #True because we created new component
        return True

# =========================================================================================================== #
def process_release_components(localization, code, quantity):
    with transaction.atomic():
        localization = Localization.objects.select_for_update().get(pk=localization.id)

        components = localization.components.all()

        existing_component = components.filter(code=code).first()

        if not existing_component:
            raise ValidationError({'message':f'Localization {localization.localization_name}'
                                             f' does not have component {code}'})

        existing_component_quantity = existing_component.quantity
        if quantity > existing_component_quantity:
            raise ValidationError({'message':f'In localization {localization.localization_name}'
                                             f' is only {existing_component_quantity} quantity of code {code} '
                                             f'you are trying to subtract {quantity}'})

        if quantity - existing_component_quantity == 0:
            existing_component.delete()
            return

        existing_component.quantity -= quantity
        existing_component.save()
        return

# =========================================================================================================== #

def process_showing_components_location(code):
    code = validate_component_code(code)

    sorted_components = Component.objects.filter(code=code).order_by('-quantity')
    return sorted_components

# =========================================================================================================== #
def process_showing_components_in_localization(localization_name):
    localization = Localization.objects.filter(localization_name=localization_name).first()

    if not localization:
        raise NotFound({'message':f'Localization {localization_name} not exists'})

    components_in_localization = localization.components.all().order_by('-quantity')
    return components_in_localization

# =========================================================================================================== #
def process_removing_components_by_admin():
    with transaction.atomic():
        all_components = Component.objects.all()
        all_components.delete()

