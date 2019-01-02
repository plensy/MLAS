from rest_framework_mongoengine import serializers
from Problematic.models import DataSource


class DataSourceSerializer(serializers.DocumentSerializer):
    class Meta:
        model = DataSource
        fields = '__all__'

