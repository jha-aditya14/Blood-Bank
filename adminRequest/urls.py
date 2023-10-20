from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('<int:user_id>/admin-request/', views.adminRequest, name='adminRequest'),
    path('<int:user_id>/request-approval/<int:requestId>/', views.requestApproval, name='requestApproval'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)