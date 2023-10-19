from django.urls import path, re_path
from . import views 
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('<int:user_id>/user-request/', views.requestTable, name='requestTable'),
    path('<int:user_id>/delete-request/<int:requestId>/', views.requestDelete, name='requestDelete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)