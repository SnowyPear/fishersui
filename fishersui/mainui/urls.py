from django.urls import path 



from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('reports/<status>/', views.reports, name='reports'),
    path('reports/<status>/<historylen>/', views.reports, name='reports'),
] 