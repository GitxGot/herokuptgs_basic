from django.urls import path
from .views import create_room, add_temperature, index

# urlpatterns = [
#     path('', views.index, name='home'),
# ]

urlpatterns = [
    path('', index, name='index'),
    path('api/room', create_room, name='create_room'),
    path('api/temperature', add_temperature, name='add_temperature'),
]