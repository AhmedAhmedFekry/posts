"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from accounts.views import log_in, log_out, SignUpView
# from django.contrib.auth.views import LogoutView, PasswordResetView, LoginView, PasswordResetDoneView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', SignUpView.as_view(), name="signup"),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('api.urls')),
    path('rest-auth/', include('rest_auth.urls')
         ), path('rest-auth/registration/', include('rest_auth.registration.urls'))
    # path('login/', log_in, name="login"),
    # path('login/', LoginView.as_view(template_name='accounts/login.html'), name="login"),
    # path('logout/', LogoutView.as_view(), name="logout"),
    # path('reset_password/', PasswordResetView.as_view(
    #     template_name='accounts/rest_password.html'), name="reset_password"),
    # path('reset_password/', PasswordResetDoneView.as_view(
    #     template_name='accounts/rest_password_done.html'), name="password_reset_confirm")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
