from rest_framework import status, generics
from ..serializers import *
from drf_yasg.utils import swagger_auto_schema

class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    @swagger_auto_schema(
        operation_summary="Список ролей",
        tags=["Role"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создание новой роли",
        tags=["Role"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RoleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    http_method_names = ['get', 'put', 'delete']

    @swagger_auto_schema(
        operation_summary="Получение роли по id",
        tags=["Role"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Полное обновление роли",
        tags=["Role"]
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частичное обновление роли",
        tags=["Role"]
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удаление роли",
        tags=["Role"]
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

