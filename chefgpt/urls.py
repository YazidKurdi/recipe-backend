from django.urls import path

from chefgpt import views

urlpatterns = [
    path('gpt-recipe/', views.ChefGPT.as_view()),
    path('gpt-usage/', views.APIUsage.as_view()),
]
