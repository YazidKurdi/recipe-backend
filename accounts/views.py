import os

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client, OAuth2Error
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class GoogleLogin(SocialLoginView):  # if you want to use Authorization Code Grant, use this
    adapter_class = GoogleOAuth2Adapter
    callback_url = f'{os.getenv("CALLBACK_URL", "http://127.0.0.1")}/accounts/google/login/callback/'
    client_class = OAuth2Client
class GetUserIdView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        return Response({'user_id': user_id})


# class FacebookLogin(SocialLoginView):
#     adapter_class = FacebookOAuth2Adapter

# class GithubLogin(SocialLoginView):
#     adapter_class = GitHubOAuth2Adapter
#     callback_url = "http://127.0.0.1:8000/accounts/github/login/callback/"
#     client_class = OAuth2Client


# class GoogleLogin(SocialLoginView): # if you want to use Authorization Code Grant, use this
#     adapter_class = GoogleOAuth2Adapter
#     callback_url = CALLBACK_URL_YOU_SET_ON_GOOGLE
#     client_class = OAuth2Client

# class CustomGoogleOAuth2Adapter(GoogleOAuth2Adapter):
#     def complete_login(self, request, app, token, response, **kwargs):
#         try:
#             print("Response : ",response["id_token"])
#             identity_data = jwt.decode(
#                 response["id_token"]["id_token"], #another nested id_token was returned
#                 options={
#                     "verify_signature": False,
#                     "verify_iss": True,
#                     "verify_aud": True,
#                     "verify_exp": True,
#                 },
#                 issuer=self.id_token_issuer,
#                 audience=app.client_id,
#             )
#         except jwt.PyJWTError as e:
#             raise OAuth2Error("Invalid id_token") from e
#         login = self.get_provider().sociallogin_from_response(request, identity_data)
#         return login
#
#
# class GoogleLogin(SocialLoginView):
#     adapter_class = CustomGoogleOAuth2Adapter
#     client_class = OAuth2Client
#     callback_url = "http://127.0.0.1:8000/accounts/google/login/callback/"

