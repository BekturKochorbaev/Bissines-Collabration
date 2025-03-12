from datetime import datetime
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, viewsets, status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Personal, Vacancy, VisitHistory, VisitHistoryComment, Award, Sticker, VacationRequest
from .serializers import PersonalCreateSerializers, \
    PersonalListSerializers, VisitHistoryCreateSerializer, PanelSerializers, \
    ProfileSerializers, PersonalUpdateDeleteSerializers, \
    VisitHistoryCommentSerializer, VisitHistoryListSerializer, AwardCreateSerializer, AwardListSerializer, \
    VacationRequestCreateSerializers, VacationRequestListSerializers

from accounts.models import UserProfile


class PersonalCreateProfileApiView(generics.CreateAPIView):
    queryset = Personal.objects.all()
    serializer_class = PersonalCreateSerializers


class PersonalUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Personal.objects.all()
    serializer_class = PersonalUpdateDeleteSerializers


class PersonalListProfileApiView(generics.ListAPIView):
    queryset = Personal.objects.all()
    serializer_class = PersonalListSerializers


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Personal.objects.all()
    serializer_class = ProfileSerializers


class PanelListAPIView(generics.ListAPIView):
    queryset = Personal.objects.all()
    serializer_class = PanelSerializers


class ProfileUpdate(APIView):

    def put(self, request, *args, **kwargs):
        email = request.user.email
        try:
            user_profile = UserProfile.objects.get(email=email)
            personal_profile = Personal.objects.get(employee=user_profile)
        except UserProfile.DoesNotExist:
            return Response({'detail': 'UserProfile не найден для этого пользователя'}, status=status.HTTP_404_NOT_FOUND)
        except Personal.DoesNotExist:
            return Response({'detail': 'Personal профиль не найден для этого пользователя'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializers(personal_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return Personal.objects.filter(id=self.request.user.id)


class StatusLeftWorkView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'personal_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID сотрудника'),
            },
            required=['personal_id']
        ),
        responses={
            200: "Время ухода зафиксировано",
            400: "Нет активной записи для фиксации ухода",
            404: "Сотрудник не найден"
        }
    )
    def post(self, request, *args, **kwargs):
        personal_id = request.data.get('personal_id')
        now = datetime.now()
        current_time = now.time()
        try:
            personal = Personal.objects.get(id=personal_id)
        except Personal.DoesNotExist:
            return Response({"error": "Сотрудник не найден"}, status=status.HTTP_404_NOT_FOUND)
        visit_history = VisitHistory.objects.filter(
            personal_status=personal,
            date=now.date(),
            status__in=["working", "lunch", "rest", "vacation", "sick_leave"]
        ).last()
        if visit_history:
            visit_history.end_time = current_time
            visit_history.status = 'left_work'
            visit_history.save()
            return Response({"message": "Время ухода зафиксировано"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Нет активной записи для фиксации ухода"}, status=status.HTTP_400_BAD_REQUEST)


class StatusWorkingView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'personal_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID сотрудника'),
            },
            required=['personal_id']
        ),
        responses={
            200: "Время прихода зафиксировано",
            400: "Нет активной записи для фиксации прихода",
            404: "Сотрудник не найден"
        }
    )
    def post(self, request, *args, **kwargs):
        personal_id = request.data.get('personal_id')
        now = datetime.now()
        current_date = now.date()
        current_time = now.time()
        try:
            personal = Personal.objects.get(id=personal_id)
        except Personal.DoesNotExist:
            return Response({"error": "Сотрудник не найден"}, status=status.HTTP_404_NOT_FOUND)
        visit_history = VisitHistory.objects.filter(
            personal_status=personal,
            date=now.date(),
            status__in=["working", "left_work"]).last()
        if visit_history:

            return Response({"error": "Нельзя зафиксировать времию второй раз"}, status=status.HTTP_404_NOT_FOUND)
        data = {
            'status': 'working',
            'date': current_date,
            'start_time': current_time,
            'personal_status': personal.id
        }
        serializer = VisitHistoryCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Время прихода зафиксировано"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VisitHistoryListAPIView(generics.ListAPIView):
    queryset = VisitHistory.objects.all()
    serializer_class = VisitHistoryListSerializer


class VisitHistoryCommentView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "user_id": openapi.Schema(type=openapi.TYPE_INTEGER, description='ID сотрудника'),
                "visit_id": openapi.Schema(type=openapi.TYPE_INTEGER, description='ID сотрудника'),
                "comment": openapi.Schema(type=openapi.TYPE_STRING, description='Оставьте коментарии'),
            },
            required=['personal_id']
        ),
        responses={
            201: "Комментарий добавлен",
            404: "Запись История посещения не найдена",
            404: "Пользователь не найден",
            404: "Комментарии можно оставлять только для записей за текущий день ",
        }
    )
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        visit_id = request.data.get('visit_id')
        comment_text = request.data.get('comment')

        current_date = datetime.now().date()
        try:
            user = Personal.objects.get(id=user_id)
        except Personal.DoesNotExist:
            return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)
        try:
            visit = VisitHistory.objects.get(id=visit_id)
        except VisitHistory.DoesNotExist:
            return Response({"error": "Запись VisitHistory не найдена"}, status=status.HTTP_404_NOT_FOUND)
        if visit.date != current_date:
            return Response({"error": "Комментарии можно оставлять только для записей за текущий день"}, status=status.HTTP_400_BAD_REQUEST)
        data = {
            'user': user.id,
            'comment': comment_text,
            'visit': visit.id
        }
        serializer = VisitHistoryCommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Комментарий добавлен"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AwardCreateView(generics.CreateAPIView): # Наградить сотрудника
    serializer_class = AwardCreateSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        sticker, created = Sticker.objects.get_or_create(
            id=self.request.data.get('sticker_id'))
        serializer.save(sticker=sticker)


class AwardListView(generics.ListAPIView): # Список награды для сотрудника
    queryset = Award.objects.all()
    serializer_class = AwardListSerializer

    def get_queryset(self):
        return Award.objects.filter(employee__employee__email=self.request.user.email)


class VacationRequestCreateView(generics.CreateAPIView):   # Форма заявки на отпуск
    serializer_class = VacationRequestCreateSerializers
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, description='Тип отпуска'),
                "from_who": openapi.Schema(type=openapi.TYPE_STRING, description='От кого'),
                "manager": openapi.Schema(type=openapi.TYPE_STRING, description='Отправить кому'),
                "start_date": openapi.Schema(type=openapi.FORMAT_DATE, description='Начало отпуски'),
                "end_date": openapi.Schema(type=openapi.FORMAT_DATE, description='Оканчание отпуски'),
                "reason": openapi.Schema(type=openapi.TYPE_STRING, description='Коментарий'),
                "document": openapi.Schema(type=openapi.TYPE_FILE, description='Документ'),
            },
            required=['status', 'from_who', 'manager', 'start_date', 'end_date', 'reason', 'document']
        ),
        consumes=["multipart/form-data"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(status='waiting')


class VacationRequestListView(generics.ListAPIView):
    queryset = VacationRequest.objects.all()
    serializer_class = VacationRequestListSerializers

# class ManagingPOListApiView(generics.ListAPIView):
#     queryset = Personal.objects.all()
#     serializer_class = ManagingPOSerializers
#
#
# class VacancyViewSet(viewsets.ModelViewSet):
#     queryset = Vacancy.objects.all()
#     serializer_class = VacancySerializers
