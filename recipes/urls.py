from django.urls import path

from recipes import views

urlpatterns = [
    path('user-recipes/', views.RecipesList.as_view()),
    path('create-recipe/', views.RecipesList.as_view()),
    path('update-recipe/<int:recipe_id>/', views.RecipesList.as_view()),
    path('delete-recipe/<int:recipe_id>/', views.RecipesList.as_view()),
    path('recipes-statistics/', views.RecipeStatistics.as_view()),
    path('all-user-recipes/', views.AllRecipesList.as_view()),
    path('list-cuisines/', views.ListCuisines.as_view()),
    # path('products/search/', views.search),
    # path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),
    # path('products/<slug:category_slug>/', views.CategoryDetail.as_view()),
]
