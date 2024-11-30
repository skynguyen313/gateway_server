from rest_framework import serializers
from .models import Person, History

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = "__all__"

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = "__all__"
