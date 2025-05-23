from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    telegram = models.CharField(max_length=100, blank=True, null=True)
    whatsapp = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    password = models.CharField(max_length=128)  # This will be hashed
    role_id = models.ForeignKey('Role', on_delete=models.CASCADE, related_name='routes',null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_pass_test = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class UserTagPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tag_preferences')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    weight = models.FloatField(default=0)

    class Meta:
        unique_together = ('user', 'tag')

class Route(models.Model):
    DIFFICULTY_CHOICES = [
        (1, 'Лёгкий'),
        (2, 'Средний'),
        (3, 'Сложный'),
        (4, 'Для профессионалов'),
    ]
    TYPES = [
        (1, 'Обустроенный'),
        (2, 'Дикий')
    ]

    id = models.AutoField(primary_key=True)
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='routes',null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    location_area = models.CharField(max_length=255)
    length_in_km = models.FloatField(null=True)
    height = models.FloatField(null=True)
    duration = models.DurationField(null=True, blank=True)
    difficulty = models.IntegerField(
        choices=DIFFICULTY_CHOICES,
        default=2,
    )
    type = models.IntegerField(
        choices=TYPES,
        default=1,
    )
    tags = models.ManyToManyField(Tag, related_name='routes', blank=True)
    is_public = models.BooleanField(default=True)
    chat_link = models.URLField(blank=True, null=True)
    views = models.IntegerField(null=True, default=0)
    gpx_url = models.FileField(upload_to='gpx_files/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class RoutePhoto(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='photos/route_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_checked = models.BooleanField(default=False)

class RouteReview(models.Model):
    id = models.AutoField(primary_key=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='route_reviews')
    rating = models.FloatField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class FavoriteRoute(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_routes')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'route')  # чтобы не было дублей

    def __str__(self):
        return f"{self.user.username} - {self.route.name}"

class MapPoint(models.Model):
    POINT_TYPES = [
        ('start', 'Стартовая точка'),
        ('camp', 'Место лагеря'),
        ('viewpoint', 'Смотровая площадка'),
        ('water', 'Источник воды'),
        ('danger', 'Опасная зона'),
        ('end', 'Конечная точка'),
        ('info', 'Информационная точка'),
    ]

    id = models.AutoField(primary_key=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='points', null=True)
    type = models.CharField(max_length=50, choices=POINT_TYPES)
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image =  models.ImageField(upload_to='photos/point_photos/', null=True)

    def __str__(self):
        return self.name


class PointReview(models.Model):
    id = models.AutoField(primary_key=True)
    point = models.ForeignKey(MapPoint, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='point_reviews')
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Item(models.Model):
    ITEM_CATEGORY = [
        ('sleeping_equipment', 'Спальное снаряжение'),
        ('kitchen_equipment', 'Кухонное снаряжение'),
        ('clothes', 'Одежда и обувь'),
        ('navigation', 'Навигация'),
        ('safety', 'Безопасность'),
        ('food', 'Еда'),
    ]


    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50, choices=ITEM_CATEGORY)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Checklist(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    route_id = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='checklists', null=True)
    pdf_url = models.FileField(upload_to='pdf_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class ChecklistItems(models.Model):
    checklist_id =  models.ForeignKey(Checklist, on_delete=models.CASCADE, related_name='items')
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='checklist_items')
    quantity = models.PositiveIntegerField()
    is_packed = models.BooleanField(default=False)
