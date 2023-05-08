from django.contrib import admin
from .models import Recipes, Ingredients,Cuisine

admin.site.register(Recipes)
admin.site.register(Ingredients)
admin.site.register(Cuisine)
