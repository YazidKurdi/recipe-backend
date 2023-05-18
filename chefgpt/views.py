import logging
import re
import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from chefgpt import utils

logger = logging.getLogger("chefgpt")
class ChefGPT(APIView):
    """
    API endpoint that generates recipes based on a given prompt using GPT-3.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'chef_gpt'

    def post(self, request, format=None):
        """
        Generates a recipe based on the provided prompt.
        """

        try:
            # Extract the recipe prompt from the HTTP request
            payload = request.data

            # Generate a recipe using GPT-3
            generated_text = utils.get_recipe(payload)

            # Remove non-ASCII characters from the generated text
            gpt_response = re.sub(r"[^\x20-\x7E]+", "", generated_text)

            # Replace single quotes with double quotes in the generated text
            # gpt_response_quotes = gpt_response.replace("'", "\"")

            # Convert the JSON-formatted generated text to a Python dictionary
            gpt_response = json.loads(gpt_response)

            # Return the generated recipe as a JSON response
            return Response(json.dumps(gpt_response), status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}. gpt_response_quotes={generated_text}")
            return Response({'error': 'An error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
