"""my_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from p_libruary.views import RegisterView, CreateUserProfile, index
from django.conf import settings
from django.conf.urls.static import static
from allauth.account.views import login, logout



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('p_libruary.urls')),
    path('', index, name='index'),
    path('accounts/', include('allauth.urls')),
    path('register/', RegisterView.as_view(
            template_name = 'register.html',
            success_url=reverse_lazy('profile-create') ), name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', CreateUserProfile.as_view(), name='profile-create')
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  