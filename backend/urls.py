from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from accounts.views import GoogleLogin #FacebookLogin, GithubLogin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('recipes.urls')),
    path('api/', include('chefgpt.urls')),
    # path('dj-rest-auth/', include('dj_rest_auth.urls')),
    # path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    # path('dj-rest-auth/google/', GoogleLogin.as_view(), name='github_login'),
    # path('accounts/', include('allauth.urls'), name='socialaccount_signup'),
    path('',include('accounts.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
