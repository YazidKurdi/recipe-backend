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

class APIUsage(APIView):
    """
    API endpoint that returns the current API usage.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'chef_gpt'

    def get(self, request):
        """
        Returns the current API usage.
        """
        try:
            throttle_instance = self.throttle_classes[0]()  # Create an instance of the throttle class

            # throttle_key = throttle_instance.get_cache_key(request, self)
            throttle_key = f"throttle_{self.throttle_scope}_{request.user.pk}"
            throttle_history = throttle_instance.cache.get(throttle_key) or []

            if throttle_history:
                throttle_history.pop(0)  # Remove the first item from the list

            throttle_instance.cache.set(throttle_key, throttle_history)  # Update the cache

            # outstanding API calls
            API_calls = len(throttle_history)

            # API calls remaining
            remaining_calls = utils.THROTTLE_RATE - API_calls

            return Response(remaining_calls, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'An error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)