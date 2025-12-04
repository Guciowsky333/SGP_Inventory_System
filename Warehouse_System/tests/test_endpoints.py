import pytest
from django.contrib.auth.models import User
from django.contrib.messages import success
from django.db.models import Sum

from Warehouse_System.models import Localization, Component
from rest_framework.test import APIClient



#<------------------------------------------- all fixture objects ---------------------------------------------->
@pytest.fixture
def test_admin_user(db):
    return User.objects.create_superuser(
        username='test_admin',
        password='123')

@pytest.fixture
def test_user(db):
    return User.objects.create_user(
        username="test_user",
        password="123"
    )
@pytest.fixture
def empty_localization(db):
    return Localization.objects.create(
        localization_name = 'P10101'
    )

@pytest.fixture
def localization_with_components(db):
    def _create(localization_obj, code, quantity):
        return Component.objects.create(
            localization = localization_obj,
            code = code,
            quantity = quantity
        )
    return _create

@pytest.fixture
def test_localization_O10101(db):
    return Localization.objects.create(
        localization_name = 'O10101',
    )

@pytest.fixture
def test_localization_O10102(db):
    return Localization.objects.create(
        localization_name='O10102',
    )

@pytest.fixture
def test_localization_O10103(db):
    return Localization.objects.create(
        localization_name='O10103',
    )

# =========================================================================================================== #
@pytest.mark.parametrize(
    'username, password, expected_status',[
        ('test_admin', '123',200),
        ('test_user', '123',200),
        ('wrong_user', 'wrong_password', 403),
    ]
)

def test_MeAPIVew(username, password, expected_status, test_user, test_admin_user):
    client = APIClient()
    client.login(username=username, password=password)


    response = client.get('/api/me/')
    assert response.status_code == expected_status

    if expected_status == 200:

        if username == 'test_admin':
            assert response.data['is_superuser'] == True

        if username == 'test_user':
            assert response.data['is_superuser'] == False

# =========================================================================================================== #
@pytest.mark.parametrize(
    'code, quantity, localization, expected_status',[
        ('7747',14,'exist',201),     #<-- correct add new component
        ('77477',14,'exist',400),     #<-- code doesn't have 4 characters
        ('ssss',14,'exist',400),     #<-- code doesn't be integer
        ('7747', 29, 'exist', 400),     #<-- too much quantity max is 28
        ('7747', 29, 'not exist', 400),    #<--  incorrect localization
    ]
)

def test_ComponentPlacementAPIView(code, quantity,localization, expected_status, test_user, empty_localization):
    if localization == 'exist':
        localization_name= empty_localization.localization_name
    else:
        localization_name = 'not_exist'
    client = APIClient()
    client.force_authenticate(user=test_user)
    body = {
        'code': code,
        'localization': localization_name,
        'quantity': quantity,
    }
    response = client.post('/api/add_components/', body, format='json')


    assert response.status_code == expected_status

    if expected_status == 200:
        empty_localization.refresh_from_db()
        assert empty_localization.components.aggregate(Sum('quantity'))['quantity__sum'] == quantity






# =========================================================================================================== #
#Case when one code is already on localization
@pytest.mark.parametrize(
    'code, quantity, expected_status',[
        (7747,8,200),   #<-- in our localization is 20 total quantity so we can add 8
        (7746,8,201),   #<-- the same situation, status is 201 because we create new component

        (7747,9,400),  #<-- Error we add 9 quantity to 20 max is 28
    ]
)
def test_ComponentPlacementAPIView_localization_with_one_code(code, quantity, expected_status, test_user, localization_with_components,empty_localization):

    #Here we are adding to empty localization component 7747, 20 quantity
    localization_with_components(empty_localization, 7747, 20)
    old_quantity = 20



    client = APIClient()
    client.force_authenticate(user=test_user)
    body = {
        'localization': empty_localization.localization_name,
        'code': code,
        'quantity': quantity
    }
    response = client.post('/api/add_components/', body, format='json')
    empty_localization.refresh_from_db()
    print(f'cos   {response.data}')
    assert response.status_code == expected_status

    if expected_status == 200:
        if code == 7747:  #<-- Case where we add the same code that already is in our localization
            assert empty_localization.components.count() == 1

            #quanity of already exist component in our localization should be equal old quantity + quantity in body
            assert Component.objects.filter(localization=empty_localization, code=code).first().quantity == old_quantity + quantity
        if code == 7746:  #<-- Case where we use new code 7746
            assert empty_localization.components.count() == 2

            #quanity of new code should be equal quantity in body
            assert Component.objects.filter(localization=empty_localization, code=code).first().quantity == quantity





# =========================================================================================================== #
#Case with two code on localization
@pytest.mark.parametrize(
    'code, quantity, expected_status',[
        (7747,1,200),   #<-- Correct because this code is already on this localization so we can add it
        (7746,1,200),   #<-- The same situation

        (7750,1,400),   #<-- Error code 7750 does not exist this localization so we can"t adn it because there are already 2 code
    ]
)
def test_ComponentPlacementAPIView_with_two_codes(code, quantity, expected_status, test_user, localization_with_components,empty_localization):

    #We are creating localization with 2 code inside 7747 and 7746
    localization_with_components(empty_localization, 7747, 5)
    localization_with_components(empty_localization, 7746, 10)
    quantity_7747 = 5
    quantity_7746 = 10
    total_quantity = 15


    client = APIClient()
    client.force_authenticate(user=test_user)
    body ={
        'localization': empty_localization.localization_name,
        'code': code,
        'quantity': quantity
    }
    response = client.post('/api/add_components/', body, format='json')
    empty_localization.refresh_from_db()

    assert response.status_code == expected_status
    if expected_status == 200:
        component = Component.objects.get(localization=empty_localization, code=code)

        #checking if quantity of already exist components was changed correct
        if code == 7747:
            assert component.quantity == quantity_7747 + quantity
        if code == 7746:
            assert component.quantity == quantity_7746 + quantity

        assert empty_localization.components.aggregate(Sum('quantity'))['quantity__sum'] == total_quantity + quantity






# =========================================================================================================== #
#Relase components with empty localization

def test_ComponentReleaseAPIView_empty_localization(empty_localization, test_user):
    client = APIClient()
    client.force_authenticate(user=test_user)
    body = {
        'localization': empty_localization.localization_name,
        'code': 7747,
        'quantity': 1
    }
    response = client.patch('/api/release_components/', body, format='json')
    assert  response.status_code == 400




# =========================================================================================================== #
@pytest.mark.parametrize(
    'code, quantity, expected_status',[
        (7747,10,200),  #<-- Correctly component release
        (7747,20,200),  #<-- Correctly component release, we delete whole quantity from localization

        (7747,21,400),  #<-- We try release too much quantity of components in this localization is only 20
        (7746,1,400),   #<-- In our localization does not have code 7746
    ]
)
def test_ComponentReleaseAPIView(code, quantity, expected_status, test_user, localization_with_components,empty_localization):

    localization_with_components(empty_localization, 7747, 20)
    quantity_7747 = 20


    client = APIClient()
    client.force_authenticate(user=test_user)
    body = {
        'localization': empty_localization.localization_name,
        'code': code,
        'quantity': quantity
    }
    response = client.patch('/api/release_components/', body, format='json')

    empty_localization.refresh_from_db()

    assert response.status_code == expected_status
    if expected_status == 200:
        component = Component.objects.filter(localization=empty_localization, code=code).first()

        #we delete whole quantity of our code from localization
        if quantity == quantity_7747:
            assert not component


        #we only delete some quantity of our code form localization
        else:
            assert component.quantity == quantity_7747 - quantity

# =========================================================================================================== #
@pytest.mark.parametrize(
    'code, expected_status',[
        (7747,200),   #<-- exist code with one localization
        (7746,200),   #<-- exist code with two localization
        (7750,200),   #<-- not exist code
        ('ssa',400),  #<-- wrong code
    ]
)

def test_ComponentShowAPIView(code,expected_status, test_user, localization_with_components, test_localization_O10101, test_localization_O10102, test_localization_O10103):
    #create all localization with components
    first_component_7747 = localization_with_components(test_localization_O10101, 7747, 20)

    first_component_7746 = localization_with_components(test_localization_O10102, 7746, 20)
    second_component_7746 = localization_with_components(test_localization_O10103, 7746, 10)


    client = APIClient()
    client.force_authenticate(user=test_user)

    first_component_7747.refresh_from_db()
    first_component_7746.refresh_from_db()
    second_component_7746.refresh_from_db()


    response = client.get(f'/api/component/{code}/localizations/')

    assert response.status_code == expected_status
    if expected_status == 200:

        #if code is correct but does not exist in warehouse
        if code == 7750:
            assert response.data['message'] == f'Code {code} does not exist in warehouse'

        #code with one localization
        if code == 7747:

            #we take first elements in data because code 7747 has exactly one localization
            data = response.data['data'][0]

            assert data['localizations'] == first_component_7747.localization.localization_name
            assert data['code'] == first_component_7747.code
            assert data['quantity'] == first_component_7747.quantity

        #code with two localizations
        if code == 7746:

            #we take all two elements in data because code 7746 has exactly two localization
            first_data = response.data['data'][0]
            second_data = response.data['data'][1]

            #The first element should be this than has larger quantity
            assert first_data['localizations'] == first_component_7746.localization.localization_name
            assert first_data['code'] == first_component_7746.code
            assert first_data['quantity'] == first_component_7746.quantity

            assert second_data['localizations'] == second_component_7746.localization.localization_name
            assert second_data['code'] == second_component_7746.code
            assert second_data['quantity'] == second_component_7746.quantity

# =========================================================================================================== #
@pytest.mark.parametrize(
    'localization_name, expected_status', [
        ('P10101', 200),  # <-- empty localization
        ('O10101', 200),  # <-- localization with one component
        ('O10102', 200),  # <-- localization with two components
        ('wrong', 404),  # <-- Not exist localization
    ]
)
def test_LocalizationShowAPIView(localization_name, expected_status, test_user, localization_with_components,
                                 empty_localization, test_localization_O10101, test_localization_O10102):

    # Adding one component in localization O10101
    localization_with_components(test_localization_O10101, 7747, 20)

    # Adding two components in localization O10102
    localization_with_components(test_localization_O10102, 7746, 10)
    localization_with_components(test_localization_O10102, 7747, 11)

    client = APIClient()
    client.force_authenticate(user=test_user)

    response = client.get(f'/api/localization/{localization_name}/components/')

    test_localization_O10101.refresh_from_db()
    test_localization_O10102.refresh_from_db()

    assert response.status_code == expected_status

    if expected_status == 200:

        #Empty localization
        if localization_name == 'P10101':
            assert response.data['data'] == []
            assert response.data['message'] == f'localization {localization_name} is empty'


        #Localization with one code
        if localization_name == 'O10101':
            assert response.data['Localization'] == 'O10101'

            first_component = response.data['data'][0]

            assert first_component['code'] == '7747'
            assert first_component['quantity'] == 20



        #Localization with two components
        if localization_name == 'O10102':
            assert response.data['Localization'] == 'O10102'

            first_component = response.data['data'][0]   #<-- First code is 7747 because we sorted components by quantity in services.py
            second_component = response.data['data'][1]  #<-- So the second is 7746

            assert first_component['code'] == '7747'
            assert first_component['quantity'] == 11

            assert second_component['code'] == '7746'
            assert second_component['quantity'] == 10

# =========================================================================================================== #
@pytest.mark.parametrize(
    'auth, expected_status', [
        ('admin', 200),
        ('user', 403),
    ]
)
def test_ComponentsRemovingAllAPIView(auth, expected_status, test_user, test_admin_user,
                                      test_localization_O10101, test_localization_O10102):

    #we create two test components to check if them will be deleting correct
    first_component = Component.objects.create(
        localization = test_localization_O10101,
        code = '7747',
        quantity = 20
    )
    second_component = Component.objects.create(
        localization = test_localization_O10102,
        code = '7746',
        quantity = 11
    )

    user = test_admin_user if auth == 'admin' else test_user

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.delete('/api/clear_warehouse/')

    assert response.status_code == expected_status

    if expected_status == 200:
        #Admin deleting all components correct
        assert Component.objects.count() == 0

    if expected_status == 403:
        #User does not have access to this endpoint so components have not been removed
        assert Component.objects.count() == 2



