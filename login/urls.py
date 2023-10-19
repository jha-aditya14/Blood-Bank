# Signin Page Urls

from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.signin, name='signin'),
    path('sign-up/', views.signup, name='signup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)