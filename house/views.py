import requests
import os
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

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



# def db(request):
#     # If you encounter errors visiting the `/db/` page on the example app, check that:
#     #
#     # When running the app on Heroku:
#     #   1. You have added the Postgres database to your app.
#     #   2. You have uncommented the `psycopg` dependency in `requirements.txt`, and the `release`
#     #      process entry in `Procfile`, git committed your changes and re-deployed the app.
#     #
#     # When running the app locally:
#     #   1. You have run `./manage.py migrate` to create the `hello_greeting` database table.

#     greeting = Greeting()
#     greeting.save()

#     greetings = Greeting.objects.all()

#     return render(request, "db.html", {"greetings": greetings})
