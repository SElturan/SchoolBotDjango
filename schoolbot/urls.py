from django.urls import path
from .views import TelegramUserViewSet, GradeViewSet, SubjectViewSet, OrderCreateView, OrderListView, OrderProcessViewSet, OrderRetrieveView, StudentViewSet, TeacherViewSet

app_name = "schoolbot"

urlpatterns = [
    path('telegram-user/', TelegramUserViewSet.as_view(
        {
            'get': 'list',
            'post': 'create'
        }
    )),
    path('telegram-user/<int:pk>/', TelegramUserViewSet.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }
    )),

    path('grade/', GradeViewSet.as_view(
        {
            'get': 'list'
        }
    )),
    path('grade/<int:pk>/', GradeViewSet.as_view(
        {
            'get': 'retrieve'
        }
    )),

    path('subject/', SubjectViewSet.as_view(
        {
            'get': 'list'
        }
    )),
    path('subject/<int:pk>/', SubjectViewSet.as_view(
        {
            'get': 'retrieve'
        }
    )),

    path('order/', OrderCreateView.as_view()),
    path('order-list/', OrderListView.as_view()),
    path('random-order/<str:subject>/', OrderRetrieveView.as_view()),

    path('order-process/', OrderProcessViewSet.as_view(
        {
            'get': 'list',
            'post': 'create'
        }
    )),

    path('order-process/<int:pk>/', OrderProcessViewSet.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }


    

    )),

    path('student/', StudentViewSet.as_view(
        {
            'get': 'list',
            'post': 'create'
        }
    )),

    
    path('student/<int:pk>/', StudentViewSet.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }
    )),


    path('teacher/', TeacherViewSet.as_view(
        {
            'get': 'list',
            'post': 'create'
        }
    )),

    path('teacher/<int:pk>/', TeacherViewSet.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }
    )),




]
