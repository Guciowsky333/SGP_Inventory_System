from django.urls import path, include
from Warehouse_System.views import (ComponentPlacementAPIView, ComponentReleaseAPIView,
                                    ComponentShowAPIView, LocalizationShowAPIView, MeAPIView,
                                    ComponentsRemovingAllAPIView)


urlpatterns = [
    path('me/', MeAPIView.as_view(), name='me'),
    path('add_components/', ComponentPlacementAPIView.as_view(), name='add_components'),
    path('release_components/', ComponentReleaseAPIView.as_view(), name='release_components'),
    path('component/<str:code>/localizations/', ComponentShowAPIView.as_view(), name='component_localizations'),
    path('localization/<str:localization_name>/components/', LocalizationShowAPIView.as_view(), name='localization_components'),
    path('clear_warehouse/', ComponentsRemovingAllAPIView.as_view(), name='clear_warehouse'),
]