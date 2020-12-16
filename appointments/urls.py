from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('schedule/<int:doc_id>', views.schedule, name='schedule')
]
