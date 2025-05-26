from django.http import FileResponse
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from ..serializers import *
from ..models import *
from drf_yasg.utils import swagger_auto_schema

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


class DownloadCheckListPdfFileView(APIView):
    @swagger_auto_schema(
        operation_summary="Получение чеклиста в формате PDF",
        tags=["Route"],
        responses={
            200: openapi.Response('PDF файл', schema=openapi.Schema(type=openapi.TYPE_FILE)),
            404: 'Файл не найден'
        }
    )
    def get(self, request,pk):
        try:
            checklist_name = self.get_checkist_name(pk)
            checklist = Checklist.objects.get(name=checklist_name)
            pdf_url = checklist.pdf_url
            if not pdf_url:
                return Response({"detail": "Файл не найден."}, status=status.HTTP_404_NOT_FOUND)

            response = FileResponse(pdf_url.open('rb'), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{pdf_url.name}"'
            return response

        except Checklist.DoesNotExist:
            return Response({"detail": "Чеклист не найден."}, status=status.HTTP_404_NOT_FOUND)

    def get_checkist_name(self, route_id):
        route = Route.objects.get(id=route_id)
        tag_names = route.tags.values_list('name', flat=True)
        if '1_день' in tag_names:
            return 'checklist_for_a_day'
        elif {'глэмпинг','укрытие'} & set(tag_names):
            return 'checklist_for_glamping'
        elif {'обустроенный'} & set(tag_names):
            return 'checklist_for_equipped_route'
        else:
            return 'wild_checklist'

class UploadCheckListPdfFileView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary="Загрузка чеклиста формата PDF",
        tags=["Checklist"],
        manual_parameters=[
            openapi.Parameter('pdf_file', openapi.IN_FORM, type=openapi.TYPE_FILE, description="PDF файл")
        ],
        responses={200: openapi.Response('Файл загружен')}
    )
    def post(self, request):
        pdf_file = request.FILES.get('pdf_file')
        if not pdf_file:
            return Response({"detail": "Файл не найден в запросе."}, status=status.HTTP_400_BAD_REQUEST)
        if not pdf_file.name.lower().endswith('.pdf'):
            return Response({"detail": "Файл должен быть в формате PDF."}, status=status.HTTP_400_BAD_REQUEST)

        name = pdf_file.name[:-4]
        try:
            checklist = Checklist.objects.get(name=name)
            if checklist:
                return Response({"detail": "Файл с таким названием уже существует."}, status=status.HTTP_400_BAD_REQUEST)
        except:
            checklist_pdf = Checklist.objects.create(
            name = name,
            pdf_url =  pdf_file
            )

        return Response({
            "detail": "Файл успешно загружен",
        }, status=status.HTTP_200_OK)
