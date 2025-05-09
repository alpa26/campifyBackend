from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    #path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('access/', access_auth_view, name='access'),
    path('user/<str:user_id>/', UserDetailView.as_view(), name='user_detail'),
    path('users/<str:username>/', UserByUsernameView.as_view(), name='user-by-username'),

    #path('users/<int:user_id>/route_reviews/', UserRouteReviewsView.as_view(), name='user-route-reviews'),
    #path('users/<int:user_id>/point_reviews/', UserPointReviewsView.as_view(), name='user-point-reviews'),
    path('users/<int:user_id>/favorite_routes/', UserFavoriteRouteReviewsView.as_view(), name='user-favorite-routes'),

    path('roles/', RoleListCreateView.as_view(), name='role-list-create'),
    path('roles/<int:pk>/', RoleRetrieveUpdateDestroyView.as_view(), name='role-detail'),
    path('routes/', RouteListCreateView.as_view(), name='route-list-create'),
    path('routes/equip/', EquipRouteGetView.as_view(), name='route-equip-list'),
    path('routes/wild/', WildRouteGetView.as_view(), name='route-wild-list'),
    path('routes/<int:pk>/', RouteRetrieveUpdateDestroyView.as_view(), name='route-detail'),
    path('routes/<int:route_id>/reviews/', RouteReviewsView.as_view(), name='route-reviews'),
    path('routes/<int:id>/upload_gpx/', UploadGpxFileView.as_view(), name='upload-gpx'),
    path('routes/<int:pk>/gpx/', GPXFileGetView.as_view(), name='route-gpx-get'),
    path('routes/<int:pk>/checklist/', DownloadCheckListPdfFileView.as_view(), name='route-checklist-get'),
    path('routes/<int:pk>/download/gpx/', GPXFileDownloadView.as_view(), name='route-gpx-download'),
    path('routes/user/<int:user_id>/', UserRouteGetView.as_view(), name='route-user'),

    path('route_photo/', RoutePhotoListCreateView.as_view(), name='route-photo-create'),
    path('route_photo/<int:pk>/', RoutePhotoRetrieveUpdateDestroyView.as_view(), name='route-photo-detail'),
    path('routes/<int:pk>/photos/', RoutePhotoByIdView.as_view(), name='route-photo-list'),
    path('route_photo/<int:id>/upload_image/', UploadRoutePhotoView.as_view(), name='upload-file'),

    path('route_reviews/', RouteReviewListCreateView.as_view(), name='route_review-list-create'),
    path('route_reviews/<int:pk>/', RouteReviewRetrieveUpdateDestroyView.as_view(), name='route_review-detail'),
    path('map_points/', MapPointListCreateView.as_view(), name='map_point-list-create'),
    path('map_points/<int:pk>/', MapPointRetrieveUpdateDestroyView.as_view(), name='map_point-detail'),
    path('map_points/<int:map_points_id>/reviews/', MapPointReviewsView.as_view(), name='point-reviews'),

    path('point_reviews/', PointReviewListCreateView.as_view(), name='point_review-list-create'),
    path('point_reviews/<int:pk>/', PointReviewRetrieveUpdateDestroyView.as_view(), name='point_review-detail'),
    path('items/', ItemListCreateView.as_view(), name='item-list-create'),
    path('items/<int:pk>/', ItemRetrieveUpdateDestroyView.as_view(), name='item-detail'),
    path('checklists/upload/', UploadCheckListPdfFileView.as_view(), name='upload-checklist'),
    path('checklists/', ChecklistListCreateView.as_view(), name='checklist-list-create'),
    path('checklists/<int:pk>/', ChecklistRetrieveUpdateDestroyView.as_view(), name='checklist-detail'),
    path('checklists/<int:checklist_id>/items/', ChecklistItemsByIdView.as_view(), name='point-reviews'),

    #path('favorite_route/', FavoriteRouteListCreateView.as_view(), name='favorite_route-detail'),
]
