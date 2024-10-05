from django.contrib import admin
from django.urls import path
from anilist import views  # Importa las vistas correctamente

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='inicio'),  # Enlaza 'home' para la página principal
    path('anime/', views.anime_list, name='anime'),
    path('manga/', views.manga_list, name='manga'),
    path('staff/', views.staff_list, name='staff'),
    path('anime/<int:anime_id>/', views.anime_detail, name='anime_detail'),
    path('manga/<int:manga_id>/', views.manga_detail, name='manga_detail'),
] 
