
from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(
        source='created_by.username', 
        read_only=True
    )
    assigned_to_name = serializers.CharField(
        source='assigned_to.username', 
        read_only=True,
        allow_null=True
    )
    
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class TaskStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('status',)

class AIDailyPlanRequestSerializer(serializers.Serializer):
    pass  # No fields needed for this simple request

