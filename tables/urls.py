from django.urls import path, re_path
from . import views 
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('<int:user_id>/tables/', views.table, name='table'),
    path('<int:user_id>/admin-tables/', views.adminTable, name='adminTable'),
    path('<int:user_id>/bloodRequests/', views.requestForBlood, name='request'),
    path('<int:user_id>/admin-bloodRequests/', views.adminRequestForBlood, name='adminRequest'),
    path('<int:user_id>/admin-addData/', views.adminAddBloodData, name='adminAddBloodData')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)