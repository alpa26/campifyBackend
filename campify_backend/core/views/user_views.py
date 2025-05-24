import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from ..serializers import *
from drf_yasg.utils import swagger_auto_schema
from django.db.models import F

@swagger_auto_schema(
    method='post',
    request_body=RegisterSerializer,
    responses={200: "Success", 400: "Bad Request"}
)
@api_view(['POST'])
@csrf_exempt
def register_view(request):
    raw_body = request.body
    data = json.loads(raw_body.decode('utf-8'))
    serializer = RegisterSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success": True}, status = 200)
    return  Response(serializer.errors, status = 400)

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email', 'password'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
    responses={200: "Success", 400: "Bad Request"}
)
@api_view(['POST'])
@csrf_exempt
def login_view(request):
    raw_body = request.body
    data = json.loads(raw_body.decode('utf-8'))
    email = data['email']
    password = data['password']
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        refresh = RefreshToken.for_user(user)
        response = JsonResponse({"message": "Login successful"})
        response.set_cookie('access_token', str(refresh.access_token), httponly=True)
        return response
    return Response({"error": "Ошибка авторизации"}, status = 400)


class UserDetailView(APIView):
    @swagger_auto_schema(
        operation_summary="Получение пользователя по id",
        tags=["User"]
    )
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class UserByUsernameView(APIView):
    @swagger_auto_schema(
        operation_summary="Получение пользователя по никнейму",
        tags=["User"]
    )
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class UserRouteReviewsView(generics.ListAPIView):
    serializer_class = RouteReviewSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return RouteReview.objects.filter(id=user_id)

    @swagger_auto_schema(
        operation_summary="Список всех отзывов пользователя к маршрутам",
        tags=["User"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class UserPointReviewsView(generics.ListAPIView):
    serializer_class = PointReviewSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return PointReview.objects.filter(id=user_id)

    @swagger_auto_schema(
        operation_summary="Список отзывов пользователя к локациям",
        tags=["User"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class UserFavoriteRouteReviewsView(generics.ListAPIView):
    serializer_class = FavoriteRouteSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return FavoriteRoute.objects.filter(id=user_id)

    @swagger_auto_schema(
        operation_summary="Список избранного пользователя",
        tags=["User"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class UserPreferencesCreateView(APIView):
    @swagger_auto_schema(
        operation_summary="Добавление тегов предпочтений пользователя по входному тестированию",
        tags=["User"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["user_id", "tags"],
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID пользователя'),
                'tags': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_STRING),
                    description="Список тегов"
                ),
            }
        )
    )
    def post(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        tags = request.data.get("tags", [])

        if not user_id or not isinstance(tags, list):
            return Response({'detail': 'user_id и tags обязательны.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

        for tag_name in tags:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            preference, created = UserTagPreference.objects.get_or_create(user=user, tag=tag)
            preference.weight = 0.5  # фиксированный вес
            preference.save()

        return Response({'detail': 'Предпочтения обновлены.'}, status=status.HTTP_200_OK)

    def update_user_preferences(self, user, route):
        STEP = 0.1  # Шаг наращивания
        tag_ids = route.tags.values_list('id', flat=True)
        self.decay_user_preferences(user, tag_ids)

        for tag_id in tag_ids:
            pref, _ = UserTagPreference.objects.get_or_create(user=user, tag_id=tag_id)
            pref.weight += STEP * (1 - pref.weight)
            pref.weight = round(min(pref.weight, 1.0), 4)
            pref.save()

    def decay_user_preferences(self, user, viewed_tag_ids, decay_rate=0.05):
        # Понижаем веса для всех тегов, которые не участвовали в текущем просмотре
        UserTagPreference.objects.filter(user=user).exclude(tag_id__in=viewed_tag_ids).update(
            weight=F('weight') * (1 - decay_rate)
        )

class UserPreferencesUpdateView(APIView):
    @swagger_auto_schema(
        operation_summary="Обновление тегов предпочтений пользователя по user_id и route_id",
        tags=["User"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["user_id", "route_id"],
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID пользователя'),
                'route_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID маршрута'),
            }
        )
    )
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        route_id = request.data.get('route_id')

        if not user_id or not route_id:
            return Response({'detail': 'user_id и route_id обязательны.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=user_id)
        route = Route.objects.get(id=route_id)


        self.update_user_preferences(user, route)
        return Response({'detail': 'Предпочтения обновлены.'}, status=status.HTTP_200_OK)

    def update_user_preferences(self, user, route):
        STEP = 0.1  # Шаг наращивания
        tag_ids = route.tags.values_list('id', flat=True)
        self.decay_user_preferences(user, tag_ids)

        for tag_id in tag_ids:
            pref, _ = UserTagPreference.objects.get_or_create(user=user, tag_id=tag_id)
            pref.weight += STEP * (1 - pref.weight)
            pref.weight = round(min(pref.weight, 1.0), 4)
            pref.save()

    def decay_user_preferences(self, user, viewed_tag_ids, decay_rate=0.05):
        # Понижаем веса для всех тегов, которые не участвовали в текущем просмотре
        UserTagPreference.objects.filter(user=user).exclude(tag_id__in=viewed_tag_ids).update(
            weight=F('weight') * (1 - decay_rate)
        )