from django.urls import path 



from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('reports/<status>/', views.missingreport, name='missingreport'),
] 