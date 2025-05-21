from rest_framework import generics
from ..serializers import *
from drf_yasg.utils import swagger_auto_schema


class TagListView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagsItemsSerializer

    @swagger_auto_schema(
        operation_summary="Список тегов",
        tags=["Tags"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)