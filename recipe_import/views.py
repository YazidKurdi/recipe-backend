import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from . import utils


logger = logging.getLogger("recipe_import")

class RecipeImport(APIView):
    """
    API endpoint that imports recipes from a given URL.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        """
        Imports a recipe from the provided URL.
        """

        try:
            # Extract the recipe URL from the HTTP request
            payload = request.data

            # Exctract URL
            url = payload.get('url')
            # Import the recipe from the URL
            imported_recipe = utils.RecipeParser(url)

            response = imported_recipe.recipe_json()

            # Return the imported recipe as a JSON response
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}.")
            return Response({'error': 'An error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)