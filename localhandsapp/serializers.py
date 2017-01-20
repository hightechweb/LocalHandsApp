from rest_framework import serializers

from localhandsapp.models import Scooper, Task

class ScooperSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    def get_logo(self, scooper):
        request = self.context.get('request')
        logo_url = scooper.logo.url

        return request.build_absolute_uri(logo_url)

    class Meta:
        model = Scooper
        fields = ("id", "name", "phone", "address", "logo")

class TasksSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Task
        fields = ("id", "name", "short_description", "price")
