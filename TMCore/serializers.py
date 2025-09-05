from rest_framework import serializers
from .models import Person, Calendar, Event

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'alias', 'email', 'phone']

class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = ['id', 'date', 'is_working_day', 'notes']

class EventSerializer(serializers.ModelSerializer):
    participants = PersonSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            'id',
            'title',
            'description',
            'start_datetime',
            'end_datetime',
            'location',
            'participants',
            'all_day'
        ]
        read_only_fields = ['id']

        extra_kwargs = {
            'participants': {'required': False}
        }

class FullCalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'start_datetime', 'end_datetime', 'location', 'participants', 'all_day']

    # Renomeando os campos para "start" e "end" (compatível com FullCalendar)
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return {
            "id": rep["id"],
            "title": rep["title"],
            "start": rep["start_datetime"],
            "end": rep["end_datetime"],
        }
