from rest_framework import serializers
from api.v1.notes.models import Note

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        # If test send patch without user
        # we get user from context and give it in validated_data
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)