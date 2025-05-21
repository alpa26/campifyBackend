from rest_framework import status, generics
from ..serializers import *
from drf_yasg.utils import swagger_auto_schema


class MapPointListCreateView(generics.ListCreateAPIView):
    queryset = MapPoint.objects.all()
    serializer_class = MapPointSerializer

    @swagger_auto_schema(
        operation_summary="Список локаций",
        tags=["MapPoint"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создание новой локации",
        tags=["MapPoint"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class MapPointRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MapPoint.objects.all()
    serializer_class = MapPointSerializer

    @swagger_auto_schema(
        operation_summary="Получение локации по id",
        tags=["MapPoint"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Полное обновление локации",
        tags=["MapPoint"]
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частичное обновление локации",
        tags=["MapPoint"]
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удаление локации",
        tags=["MapPoint"]
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class MapPointReviewsView(generics.ListAPIView):
    serializer_class = PointReviewSerializer

    def get_queryset(self):
        map_points_id = self.kwargs['map_points_id']
        return PointReview.objects.filter(id=map_points_id)

    @swagger_auto_schema(
        operation_summary="Список отзывов локации",
        tags=["MapPoint"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

# Отзывы к локациям
class PointReviewListCreateView(generics.ListCreateAPIView):
    queryset = PointReview.objects.all()
    serializer_class = PointReviewSerializer
    http_method_names = ['post']

    @swagger_auto_schema(
        operation_summary="Список отзывов",
        tags=["PointReview"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создание нового отзыва",
        tags=["PointReview"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class PointReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PointReview.objects.all()
    serializer_class = PointReviewSerializer
    http_method_names = ['get', 'put', 'delete']

    @swagger_auto_schema(
        operation_summary="Получение отзыва по id",
        tags=["PointReview"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Полное обновление отзыва",
        tags=["PointReview"]
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частичное обновление отзыва",
        tags=["PointReview"]
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удаление отзыва",
        tags=["PointReview"]
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)