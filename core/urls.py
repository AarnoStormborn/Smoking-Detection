from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('alerts', views.alertsList, name='alerts'),
    path('stream/<int:pk>', views.stream, name='stream'),
    path('delete/<int:pk>', views.deleteSample, name='delete')
]