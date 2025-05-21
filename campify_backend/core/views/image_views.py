from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from ..serializers import *
from ..models import *
from drf_yasg.utils import swagger_auto_schema

# Фото к маршрутам

class RoutePhotoListView(generics.ListCreateAPIView):
    queryset = RoutePhoto.objects.all()
    serializer_class = RoutePhotoSerializer
    http_method_names = ['get']

    def get_queryset(self):
        return RoutePhoto.objects.filter(is_checked=True)

    @swagger_auto_schema(
        operation_summary="Список всех фото к маршрутам",
        tags=["RoutePhoto"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class RoutePhotoUnchekedListView(generics.ListCreateAPIView):
    queryset = RoutePhoto.objects.all()
    serializer_class = RoutePhotoSerializer
    http_method_names = ['get']

    def get_queryset(self):
        return RoutePhoto.objects.filter(is_checked=False)

    @swagger_auto_schema(
        operation_summary="Список всех непроверенных фото",
        tags=["RoutePhoto"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class RoutePhotoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RoutePhoto.objects.all()
    serializer_class = RoutePhotoSerializer
    http_method_names = ['delete']

    @swagger_auto_schema(
        operation_summary="Удалить фото маршрута",
        tags=["RoutePhoto"]
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class UpdatePhotoValidationStatusView(APIView):
    serializer_class = ValidationRoutePhotoSerializer

    @swagger_auto_schema(
        operation_summary="Изменить статус фото к маршруту",
        request_body=ValidationRoutePhotoSerializer,
        tags=["RoutePhoto"]
    )
    def patch(self, request, pk):
        try:
            photo = RoutePhoto.objects.get(pk=pk)
        except RoutePhoto.DoesNotExist:
            return Response({"detail": "Photo not found"}, status=status.HTTP_404_NOT_FOUND)

        is_checked = request.data.get('is_checked')
        if is_checked is None:
            return Response({"detail": "'is_checked' field is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Обновляем поле
        photo.is_checked = bool(is_checked)
        photo.save()

        return Response({"id": photo.id, "is_checked": photo.is_checked}, status=status.HTTP_200_OK)

class RoutePhotoByIdView(generics.ListAPIView):
    serializer_class = RoutePhotoSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return RoutePhoto.objects.filter(route=pk, is_checked = True)

    @swagger_auto_schema(
        operation_summary="Получить фото маршрута по id",
        tags=["Route"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UploadRoutePhotoView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary="Загрузка изображения по ID маршрута",
        tags=["RoutePhoto"],
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID маршрута", type=openapi.TYPE_INTEGER),
            openapi.Parameter('image', openapi.IN_FORM, type=openapi.TYPE_FILE, description="Фото маршрута"),
        ],
        responses={201: openapi.Response('Фото успешно загружено')}
    )
    def post(self, request, id):
        try:
            route = Route.objects.get(id=id)
        except Route.DoesNotExist:
            return Response({"detail": "Маршрут не найден."}, status=status.HTTP_404_NOT_FOUND)

        image = request.FILES.get('image')
        if not image:
            return Response({"detail": "Файл не найден в запросе."}, status=status.HTTP_400_BAD_REQUEST)

        photo = RoutePhoto.objects.create(route=route, image=image)

        return Response({
            "detail": "Фото успешно загружено.",
            "photo_id": photo.id,
            "image_url": photo.image.url
        }, status=status.HTTP_201_CREATED)

# Фото к локациям

class DeleteMapPointImageView(APIView):
    @swagger_auto_schema(
        operation_summary="Удалить изображение у локации",
        tags=["MapPoint"]
    )
    def delete(self, request, pk):
        try:
            point = MapPoint.objects.get(id=pk)
        except MapPoint.DoesNotExist:
            return Response(
                {"detail": "Локация не найдена."},
                status=status.HTTP_404_NOT_FOUND
            )

        if not point.image:
            return Response(
                {"detail": "У этой точки нет изображения."},
                status=status.HTTP_404_NOT_FOUND
            )

        point.image.delete(save=False)
        point.image = None
        point.save()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

class MapPointPhotoByIdView(generics.ListAPIView):
    serializer_class = RoutePhotoSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return RoutePhoto.objects.filter(route=pk)

    @swagger_auto_schema(
        operation_summary="Получить фото локации по id",
        tags=["MapPoint"]
    )
    def get(self, request, *args, **kwargs):
        try:
            pk = self.kwargs.get('pk')
            map_point = MapPoint.objects.get(id=pk)
        except MapPoint.DoesNotExist:
            return Response({"detail": "Точка маршрута не найдена."}, status=status.HTTP_404_NOT_FOUND)

        if not map_point.image:
            return Response({"detail": "Фото для этой точки не найдено."}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "image_url": map_point.image.url
        }, status=status.HTTP_201_CREATED)


class UploadMapPointPhotoView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary="Загрузка изображения по ID локации",
        tags=["MapPoint"],
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID маршрута", type=openapi.TYPE_INTEGER),
            openapi.Parameter('image', openapi.IN_FORM, type=openapi.TYPE_FILE, description="Фото локации"),
        ],
        responses={201: openapi.Response('Фото успешно загружено')}
    )
    def post(self, request, pk):
        try:
            point = MapPoint.objects.get(id=pk)
        except Route.DoesNotExist:
            return Response({"detail": "Локация не найдена!"}, status=status.HTTP_404_NOT_FOUND)

        image = request.FILES.get('image')
        if not image:
            return Response({"detail": "Файл не найден в запросе!"}, status=status.HTTP_400_BAD_REQUEST)

        if point.image:
            point.image.delete(save=False)

        point.image = image
        point.save()

        return Response({
            "detail": "Фото успешно загружено.",
            "photo_id": point.id,
            "image_url": point.image.url
        }, status=status.HTTP_201_CREATED)
