import re

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


def create_tags_for_route(data):
    tags = []

    if data.get('difficulty') == 1:
        tags.append('новичок')
        tags.append('легко')
    elif data.get('difficulty') == 2:
        tags.append('средне')
    elif data.get('difficulty') == 3:
        tags.append('опытный')
        tags.append('сложно')
    elif data.get('difficulty') == 4:
        tags.append('профи')
        tags.append('сложно')

    if data.get('type') == 1:
        tags.append('обустроенный')
    elif data.get('type') == 2:
        tags.append('дикий')
        tags.append('экстрим')

    if data.get('duration'):
        duration = data['duration']
        total_hours = duration.total_seconds() // 3600
        if total_hours <= 8:
            tags.append('1_день')
        elif 8 < total_hours <= 18:
            tags.append('выходные')
        elif 18 < total_hours <= 150:
            tags.append('неделя')
        else:
            tags.append('экспедиция')

    text = f"{data.get('description', '') or ''} {data.get('name', '') or ''}".lower()

    if 'пешком' in text or 'пеший' in text or 'ногами' in text:
        tags.append('пеший')
    if 'сплав' in text or 'байдарк' in text or 'SUP' in text:
        tags.append('сплав')
    if 'фото' in text or 'пейзаж' in text:
        tags.append('фото')
    if 'пещер' in text or 'ущель' in text:
        tags.append('пещеры')
    if 'йог' in text or 'медитац' in text:
        tags.append('релакс')

    if 'глэмпинг' in text:
        tags.append('глэмпинг')
        tags.append('укрытие')
    if 'кемпинг' in text:
        tags.append('кемпинг')


    if 'машин' in text or 'авто' in text or 'колес' in text:
        tags.append('комфорт_авто')
        tags.append('транспорт')

    if 'аренда' in text:
        if 'палатка' in text or 'спальник' in text:
            tags.append('аренда_снаряжение')
        if 'газов' in text or 'горелк' in text:
            tags.append('аренда_кухня')
        if 'байдар' in text or 'велосипед' in text:
            tags.append('аренда_транспорт')
    else:
        tags.append('без_аренды')

    if 'гора' in text or 'горы' in text:
        tags.append('горы')
    if 'озер' in text or 'рек' in text or 'мор' in text  or 'водоем' in text:
        tags.append('вода')
    if 'лес' in text or re.search(r'\bрощ[аеиуыюя]\b', text) or 'бор' in text:
        tags.append('лес')
    if 'истор' in text or 'заброшк' in text or 'петроглиф' in text:
        tags.append('история')
    if 'малоизвест' in text or 'секрет' in text:
        tags.append('секретные')

    if 'один' in text or 'друзья' in text:
        tags.append('взрослые')
    if (re.search(r'\bдет(и|ям|ями|ях)\b', text) or
            re.search(r'\bреб(ё|е)н(ка|ок|ку|ке)\b', text)):
        tags.append('дети')
    if 'собак' in text or 'пёс' in text:
        tags.append('с_собакой')
    if 'групп' in text or 'гид' in text:
        tags.append('группа')

    if 'летом' in text or 'лет' in text:
        tags.append('лето')
    if 'осень' in text:
        tags.append('осень')
    if 'зим' in text:
        tags.append('зима')
    if 'весн' in text:
        tags.append('весна')

    if 'экстрим' in text:
        tags.append('экстрим')
    if 'природ' in text:
        tags.append('природа')
    if 'культур' in text:
        tags.append('культура')

    return tags


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

        instance = serializer.instance
        tags = create_tags_for_route(serializer.validated_data)
        tag_objs = [Tag.objects.get_or_create(name=tag)[0] for tag in tags]
        instance.tags.set(tag_objs)

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