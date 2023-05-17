from django.urls import path

from recipe_import import views

urlpatterns = [
    path('recipe-import/', views.RecipeImport.as_view())
]
