from django.urls import path

from accounts import views

urlpatterns = [
    path('get-userid/', views.GetUserIdView.as_view()),
]
