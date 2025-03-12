from django.urls import path

from .views import PersonalCreateProfileApiView, PersonalUpdateDeleteApiView, VacationRequestListView, \
    PersonalListProfileApiView, PanelListAPIView, StatusWorkingView, StatusLeftWorkView, \
    VisitHistoryListAPIView, ProfileViewSet, ProfileUpdate, VisitHistoryCommentView, AwardCreateView, AwardListView, \
    VacationRequestCreateView

urlpatterns = [
    path('personal-list/', PersonalListProfileApiView.as_view(), name="personal_list"),
    path('personal-create/', PersonalCreateProfileApiView.as_view(), name="personal_create"),
    path('personal-list/<int:pk>/', PersonalUpdateDeleteApiView.as_view(), name="personal_update"),
    path('panel_working_hours/', PanelListAPIView.as_view(), name='A panel for tracking employees working hours'),
    path('award-create/', AwardCreateView.as_view(), name='comment-create'),

    # For Employees--------------

    path('status-working/', StatusWorkingView.as_view(), name='status-working'),
    path('status-left_work/', StatusLeftWorkView.as_view(), name='status-left-work'),
    path('visit-history/', VisitHistoryListAPIView.as_view(), name='visit-history'), # История посещения
    path('comment-create/', VisitHistoryCommentView.as_view(), name='comment-create'), # Коментарии сорудников
    path('employee-profile/', ProfileViewSet.as_view({'get': 'list'}), name='profile'),
    path('employee-profile-update/', ProfileUpdate.as_view(), name='profile'),
    path('award-list/', AwardListView.as_view(), name='award-list'),
    path('vacation-request-create/', VacationRequestCreateView.as_view(), name='vacation-request-create'),  # Форма заявки на отпуск
    path('vacation-request-list/', VacationRequestListView.as_view(), name='vacation-request-list'),  # Форма заявки на отпуск




]