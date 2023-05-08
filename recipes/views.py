from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Recipes, Cuisine
from .serializers import RecipeSerializer, AllRecipeSerializer, CuisineSerializer

from recipes import RecipesPagination



class RecipesList(APIView):


    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        API view to retrieve a list of recipes created by the authenticated user
        """
        # Retrieve recipes created by the authenticated user
        recipes = Recipes.objects.filter(author_id=request.user.id)
        total_recipes = recipes.count()

        # Get the page number from the query parameters
        page = request.query_params.get('page')

        # Check if the page parameter is None
        if page is None:
            # If page is None, get all recipes
            serializer = RecipeSerializer(recipes, many=True)
            response = Response(serializer.data)
        else:
            # If page is not None, follow the existing logic to paginate the recipes
            paginator = RecipesPagination()
            result_page = paginator.paginate_queryset(recipes, request)
            serializer = RecipeSerializer(result_page, many=True)
            response = paginator.get_paginated_response(serializer.data)
            # Add a custom header with the total number of recipes
            response['X-Total-Count'] = total_recipes


        # Return the paginated response or all recipes
        return response


    def post(self, request, format=None):
        """
        API view to create a new recipe for the authenticated user
        """
        # Serialize the request data
        serializer = RecipeSerializer(data=request.data)

        # Check if the serializer is valid
        if serializer.is_valid():
            # Save the recipe
            serializer.save()
            # Return the serialized data with a success status code
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Return the serializer errors with a bad request status code
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self,request,recipe_id):
        """
        API view to update an existing recipe for the authenticated user
        """
        # Retrieve the recipe to be updated
        recipe = Recipes.objects.get(pk=recipe_id)

        # Serialize the updated recipe data
        serializer = RecipeSerializer(recipe,data=request.data)

        # Check if the serializer is valid
        if serializer.is_valid():
            # Save the updated recipe
            serializer.save()
            # Return the serialized data
            return Response(serializer.data)
        # Return the serializer errors with a bad request status code
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,recipe_id):
        """
        API view to delete an existing recipe for the authenticated user
        """
        # Retrieve the recipe to be deleted
        recipe = Recipes.objects.get(pk=recipe_id)

        # Delete the recipe
        recipe.delete()

        # Return a success status code
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeStatistics(APIView):

    def get(self, request, format=None):
        """
        API view to return a JSON response containing the total number of recipes, users and ingredients in the database.
        """
        recipe_count = Recipes.objects.all().count()
        user_count = Recipes.objects.all().values('author_id').distinct().count()
        ingredients_count = Recipes.objects.all().values('ingredients').distinct().count()

        return Response({'recipe_count': recipe_count, 'user_count': user_count, 'ingredient_count': ingredients_count})


class AllRecipesList(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        API view to return a JSON response containing a list of all recipes created by the authenticated user.
        """
        recipes = Recipes.objects.filter(author_id=request.user.id)

        serializer = AllRecipeSerializer(recipes, many=True)
        response = Response(serializer.data)

        return response


class ListCuisines(APIView):

    def get(self, request, format=None):
        """
        API view to return a JSON response containing a list of all cuisines in the database, ordered by name.
        """
        cuisines = Cuisine.objects.all().order_by('name')
        serializer = CuisineSerializer(cuisines, many=True)
        return Response(serializer.data)
