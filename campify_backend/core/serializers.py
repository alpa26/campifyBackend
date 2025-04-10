from rest_framework import serializers
from .models import *


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email','phone','telegram','whatsapp','description','role_id','created_at','last_login')

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'

class RouteReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteReview
        fields = '__all__'

class FavoriteRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteRoute
        fields = '__all__'

class MapPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapPoint
        fields = '__all__'

class PointReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointReview
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class ChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checklist
        fields = '__all__'