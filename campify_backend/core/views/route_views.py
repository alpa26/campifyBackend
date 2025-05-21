from django.db.models import Avg, F, Sum, Case, When, FloatField, Value
from django.http import FileResponse
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from ..serializers import *
from ..models import *
from drf_yasg.utils import swagger_auto_schema

class RouteListCreateView(generics.ListCreateAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def get_queryset(self):
        return Route.objects.filter(is_public=True).annotate(average_rating=Avg('reviews__rating'))

    @swagger_auto_schema(
        operation_summary="Список маршрутов",
        tags=["Route"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создание нового маршрута",
        tags=["Route"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # Возвращаем только ID
        return Response({'id': serializer.instance.id}, status=status.HTTP_201_CREATED)


class UserRouteGetView(generics.ListAPIView):
    serializer_class = RouteSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Route.objects.filter(author=user_id).annotate(average_rating=Avg('reviews__rating'))

    @swagger_auto_schema(
        operation_summary="Список маршрутов пользователя",
        tags=["Route"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class EquipRouteGetView(generics.ListAPIView):
    serializer_class = RouteSerializer

    def get_queryset(self):
        return Route.objects.filter(type = 1, is_public=True)

    @swagger_auto_schema(
        operation_summary="Список оборудованных маршрутов",
        tags=["Route"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class WildRouteGetView(generics.ListAPIView):
    serializer_class = RouteSerializer

    def get_queryset(self):
        return Route.objects.filter(type = 2, is_public=True)

    @swagger_auto_schema(
        operation_summary="Список диких маршрутов",
        tags=["Route"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class RecommendedRoutesView(generics.ListAPIView):
    serializer_class = RouteSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if not user_id:
            return Route.objects.none()

        user = User.objects.get(id=user_id)

        preferences = UserTagPreference.objects.filter(user=user)

        if not preferences.exists():
            return Route.objects.filter(is_public=True).order_by('-views')[:10]  # fallback

        whens = [
            When(tags=pref.tag, then=Value(pref.weight))
            for pref in preferences
        ]

        return (
            Route.objects
            .filter(is_public=True, tags__in=[p.tag for p in preferences])
            .annotate(score=Sum(
                Case(*whens, output_field=FloatField())
            ))
            .order_by('-score', '-views')
            .distinct()
        )

    @swagger_auto_schema(
        operation_summary="Список рекомендованных маршрутов для пользователя",
        tags=["Route"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class RouteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    @swagger_auto_schema(
        operation_summary="Получение маршрута по id",
        tags=["Route"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Полное обновление маршрута",
        tags=["Route"]
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частичное обновление маршрута",
        tags=["Route"]
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удаление маршрута",
        tags=["Route"]
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class RouteReviewsView(generics.ListAPIView):
    serializer_class = RouteReviewSerializer

    def get_queryset(self):
        route_id = self.kwargs['route_id']
        return RouteReview.objects.filter(route=route_id)

    @swagger_auto_schema(
        operation_summary="Список отзывов маршрута",
        tags=["Route"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# FavoriteRoute
class FavoriteRouteListCreateView(generics.ListCreateAPIView):
    queryset = FavoriteRoute.objects.all()
    serializer_class = FavoriteRouteSerializer

    @swagger_auto_schema(
        operation_summary="Список избранных маршрутов",
        tags=["FavoriteRoute"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Добавление маршрута в избранное",
        tags=["FavoriteRoute"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RouteReviewListCreateView(generics.ListCreateAPIView):
    queryset = RouteReview.objects.all()
    serializer_class = RouteReviewSerializer
    http_method_names = ['post']

    @swagger_auto_schema(
        operation_summary="Полный список отзывов к маршруту",
        tags=["RouteReview"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создание нового отзыва к маршруту",
        tags=["RouteReview"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class RouteReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RouteReview.objects.all()
    serializer_class = RouteReviewSerializer
    http_method_names = ['get', 'put', 'delete']

    @swagger_auto_schema(
        operation_summary="Получение отзыва к маршруту по id",
        tags=["RouteReview"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Полное обновление отзыва к маршруту",
        tags=["RouteReview"]
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частичное обновление отзыва к маршруту",
        tags=["RouteReview"]
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удаление отзыва к маршруту",
        tags=["RouteReview"]
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)



class UploadGpxFileView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary="Загрузка GPX-файла по ID маршрута",
        tags=["Route"],
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID маршрута", type=openapi.TYPE_INTEGER),
            openapi.Parameter('gpx_file', openapi.IN_FORM, type=openapi.TYPE_FILE, description="GPX файл")
        ],
        responses={200: openapi.Response('Файл загружен')}
    )
    def post(self, request, id):
        try:
            route = Route.objects.get(id=id)
        except Route.DoesNotExist:
            return Response({"detail": "Маршрут не найден."}, status=status.HTTP_404_NOT_FOUND)

        gpx_file = request.FILES.get('gpx_file')
        if not gpx_file:
            return Response({"detail": "Файл не найден в запросе."}, status=status.HTTP_400_BAD_REQUEST)

        route.gpx_url = gpx_file
        route.save()

        return Response({
            "detail": "Файл успешно загружен",
            "gpx_url": route.gpx_url.url
        })


class GPXFileDownloadView(APIView):
    @swagger_auto_schema(
        operation_summary="Скачивание GPX файла маршрута",
        tags=["Route"],
        responses={
            200: openapi.Response(
                description="GPX файл",
                schema=openapi.Schema(type=openapi.TYPE_FILE),
            ),
            404: "Файл не найден",
        },
    )
    def get(self, request, pk):
        try:
            route = Route.objects.get(pk=pk)
            gpx_file = route.gpx_url
            if not gpx_file:
                return Response({"detail": "Файл не найден."}, status=status.HTTP_404_NOT_FOUND)

            response = FileResponse(gpx_file.open('rb'), content_type='application/gpx+xml')
            response['Content-Disposition'] = f'attachment; filename="{gpx_file.name}"'
            return response

        except Route.DoesNotExist:
            return Response({"detail": "Маршрут не найден."}, status=status.HTTP_404_NOT_FOUND)


class GPXFileGetView(APIView):
    @swagger_auto_schema(
        operation_summary="Получение GPX файла маршрута",
        tags=["Route"],
        responses={
            200: openapi.Response(
                description="GPX файл",
                schema=openapi.Schema(type=openapi.TYPE_FILE),
            ),
            404: "Файл не найден",
        },
    )
    def get(self, request, pk):
        try:
            route = Route.objects.get(pk=pk)
            gpx_file = route.gpx_url
            if not gpx_file:
                return Response({"detail": "Файл не найден."}, status=status.HTTP_404_NOT_FOUND)
            return FileResponse(gpx_file.open('rb'), content_type='application/gpx', filename=gpx_file.name)
        except Route.DoesNotExist:
            return Response({"detail": "Маршрут не найден."}, status=status.HTTP_404_NOT_FOUND)