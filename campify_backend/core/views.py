from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import *
from .serializers import *

from .serializers import RegisterSerializer

class UserDetailView(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

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
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, email=username, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            response = JsonResponse({"message": "Login successful"})
            response.set_cookie('access_token', str(refresh.access_token), httponly=True)
            return response
    return render(request, 'login.html')

# Role
class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class RoleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


# Route
class RouteListCreateView(generics.ListCreateAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

class RouteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


# RouteReview
class RouteReviewListCreateView(generics.ListCreateAPIView):
    queryset = RouteReview.objects.all()
    serializer_class = RouteReviewSerializer

class RouteReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RouteReview.objects.all()
    serializer_class = RouteReviewSerializer



# MapPoint
class MapPointListCreateView(generics.ListCreateAPIView):
    queryset = MapPoint.objects.all()
    serializer_class = MapPointSerializer

class MapPointRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MapPoint.objects.all()
    serializer_class = MapPointSerializer

# PointReview
class PointReviewListCreateView(generics.ListCreateAPIView):
    queryset = PointReview.objects.all()
    serializer_class = PointReviewSerializer

class PointReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PointReview.objects.all()
    serializer_class = PointReviewSerializer


# Item
class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

# Checklist
class ChecklistListCreateView(generics.ListCreateAPIView):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer

class ChecklistRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer








