import requests
import os
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg, Count

from .models import Room, Temperature

# Create your views here.


def index(request):
    return render(request, 'index.html')

@csrf_exempt
def create_room(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            if not name:
                return JsonResponse({'message': 'Room name is required.'}, status=400)

            room, created = Room.objects.get_or_create(name=name)
            if created:
                return JsonResponse({'message': f'Room "{room.name}" created successfully!'})
            else:
                return JsonResponse({'message': f'Room "{room.name}" already exists.'}, status=400)

        except Exception as e:
            return JsonResponse({'message': 'Error creating room.', 'error': str(e)}, status=500)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)

@csrf_exempt
def add_temperature(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            room_id = data.get('room')
            temperature = data.get('temperature')
            date = data.get('date')  # optional

            if not all([room_id, temperature]):
                return JsonResponse({'message': 'Room ID and temperature are required.'}, status=400)

            room = Room.objects.get(id=room_id)

            if date:
                from django.utils.dateparse import parse_datetime
                dt = parse_datetime(date)
                if not dt:
                    return JsonResponse({'message': 'Invalid date format.'}, status=400)
                Temperature.objects.create(room=room, temperature=temperature, date=dt)
            else:
                Temperature.objects.create(room=room, temperature=temperature)

            return JsonResponse({'message': f'Temperature added for room "{room.name}".'})
        except Room.DoesNotExist:
            return JsonResponse({'message': 'Room not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'message': 'Error adding temperature.', 'error': str(e)}, status=500)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)


@csrf_exempt
def get_room_average(request, room_id):
    if request.method == 'GET':
        try:
            room = Room.objects.get(id=room_id)
            temperatures = Temperature.objects.filter(room=room)

            if not temperatures.exists():
                return JsonResponse({'message': 'No temperature data for this room.'}, status=404)

            avg_temp = temperatures.aggregate(Avg('temperature'))['temperature__avg']
            # Count distinct days
            days_count = temperatures.dates('date', 'day').count()

            return JsonResponse({
                'name': room.name,
                'average': round(avg_temp, 2),
                'days': days_count
            })

        except Room.DoesNotExist:
            return JsonResponse({'message': 'Room not found.'}, status=404)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)
