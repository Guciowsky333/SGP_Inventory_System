from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.response import Response
from  rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from Warehouse_System.models import Component, Localization
from Warehouse_System.serializers import ComponentSerializer
from Warehouse_System.services import (process_component_placement, process_release_components,
                                       process_showing_components_location,
                                       process_showing_components_in_localization, process_removing_components_by_admin)

# Create your views here.


class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'is_superuser': request.user.is_superuser,
        }, status=status.HTTP_200_OK)



class ComponentPlacementAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.data['localization'] = request.data['localization'].upper()
        serializer = ComponentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data


        localization = validated_data['localization']
        code = validated_data['code']
        quantity = validated_data['quantity']


        created_component = process_component_placement(localization, code, quantity)


        response_status = status.HTTP_201_CREATED if created_component else status.HTTP_200_OK




        return Response({'message':f'Adding code {code} on localization '
                                   f'{localization.localization_name} was successful'},status=response_status)





class ComponentReleaseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = ComponentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        localization = validated_data['localization']
        code = validated_data['code']
        quantity = validated_data['quantity']

        process_release_components(localization, code, quantity)

        return Response({'message':f'Issuing code {code} was successful'},status=status.HTTP_200_OK)




class ComponentShowAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, code):
        all_sorted_localizations = process_showing_components_location(code)

        #if code not exist in warehouse
        if not all_sorted_localizations:
            return Response({'message':f'Code {code} does not exist in warehouse'},status=status.HTTP_200_OK)


        data = [{
            'localizations': component.localization.localization_name,
            'code': component.code,
            'quantity': component.quantity
        }
        for component in all_sorted_localizations ]
        return Response({'data': data}, status=status.HTTP_200_OK)




class LocalizationShowAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, localization_name):
        components_in_localization = process_showing_components_in_localization(localization_name.upper())

        if not components_in_localization:
            return Response({'data':[], 'message':f'localization {localization_name} is empty'},status=status.HTTP_200_OK)

        data = [{
            'code': component.code,
            'quantity': component.quantity
        }
        for component in components_in_localization]

        return Response({'Localization':f'{localization_name.upper()}', 'data': data}, status=status.HTTP_200_OK)




class ComponentsRemovingAllAPIView(APIView):
    permission_classes = [IsAdminUser]
    def delete(self, request):
        process_removing_components_by_admin()
        return Response({'message':'All components have been removed'},status=status.HTTP_200_OK)

