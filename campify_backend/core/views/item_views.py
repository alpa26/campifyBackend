from rest_framework import generics
from ..serializers import *
from drf_yasg.utils import swagger_auto_schema

class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    @swagger_auto_schema(
        operation_summary="Список предметов",
        tags=["Item"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создание нового предмета",
        tags=["Item"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class ItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    @swagger_auto_schema(
        operation_summary="Получение предмета по id",
        tags=["Item"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Полное обновление предмета",
        tags=["Item"]
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частичное обновление предмета",
        tags=["Item"]
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удаление предмета",
        tags=["Item"]
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)