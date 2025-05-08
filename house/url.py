from django.urls import path
from .views import index, create_room, add_temperature, get_room_average

urlpatterns = [
    path('', index, name='index'),
    path('api/room', create_room, name='create_room'),
    path('api/temperature', add_temperature, name='add_temperature'),
    path('api/room/<int:room_id>', get_room_average, name='get_room_average'),

]