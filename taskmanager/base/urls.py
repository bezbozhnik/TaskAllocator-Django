from django.urls import path

from . import views
app_name = 'base'
urlpatterns = [
    path("", views.index, name="index"),
    path('login/', views.loginPage, name='login'),
    path('registration/', views.registrationPage, name='registration'),
    path('hierarchy/', views.hierarchyPage, name='hierarchy'),
]