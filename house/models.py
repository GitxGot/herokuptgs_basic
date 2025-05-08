from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

class Temperature(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='temperatures')
    temperature = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.temperature}°C in {self.room.name} on {self.date.strftime('%Y-%m-%d %H:%M:%S')}"
