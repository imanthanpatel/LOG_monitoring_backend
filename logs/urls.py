from django.urls import path
from .views import LogListView,AlertListView,DashboardView

urlpatterns = [
    path('logs/', LogListView.as_view()),
    path('alerts/', AlertListView.as_view()),
    path('dashboard/', DashboardView.as_view()),
]