from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import *
from .serializers import RegisterSerializer
from drf_yasg.utils import swagger_auto_schema

def access_auth_view(request):
    return render(request, 'access.html')

def home_view(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return redirect('login')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            response = JsonResponse({"message": "Login successful"})
            response.set_cookie('access_token', str(refresh.access_token), httponly=True)
            return response
    return render(request, 'login.html')


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

# Role

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


# Route
class RouteListCreateView(generics.ListCreateAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

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

class UploadGpxFileView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary="Загрузка GPX-файла по ID маршрута",
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


class RouteReviewsView(generics.ListAPIView):
    serializer_class = RouteReviewSerializer

    def get_queryset(self):
        route_id = self.kwargs['route_id']
        return RouteReview.objects.filter(id=route_id)

    @swagger_auto_schema(
        operation_summary="Список отзывов маршрута",
        tags=["Route"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# RouteReview
class RouteReviewListCreateView(generics.ListCreateAPIView):
    queryset = RouteReview.objects.all()
    serializer_class = RouteReviewSerializer
    http_method_names = ['post']

    @swagger_auto_schema(
        operation_summary="Полный список отзывов",
        tags=["RouteReview"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создание нового отзыва",
        tags=["RouteReview"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class RouteReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RouteReview.objects.all()
    serializer_class = RouteReviewSerializer
    http_method_names = ['get', 'put', 'delete']

    @swagger_auto_schema(
        operation_summary="Получение отзыва по id",
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

# MapPoint
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

# PointReview
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

# Item
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

# Checklist
class ChecklistListCreateView(generics.ListCreateAPIView):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer

    @swagger_auto_schema(
        operation_summary="Список чек-листов",
        tags=["Checklist"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создание нового чек-листа",
        tags=["Checklist"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class ChecklistRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer

    @swagger_auto_schema(
        operation_summary="Получение чек-листа по id",
        tags=["Checklist"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Полное обновление чек-листа",
        tags=["Checklist"]
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частичное обновление чек-листа",
        tags=["Checklist"]
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удаление чек-листа",
        tags=["Checklist"]
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class ChecklistItemsByIdView(generics.ListAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        checklist_id = self.kwargs['checklist_id']
        checklist =  Checklist.objects.get(id=checklist_id)
        return checklist.items.all()

    @swagger_auto_schema(
        operation_summary="Список вещей чек-листа по id",
        tags=["Checklist"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)









