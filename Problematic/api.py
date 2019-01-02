from Problematic.serializers import DataSourceSerializer
from Problematic.models import DataSource
from rest_framework_mongoengine import viewsets as meviewsets


class ProblematicViewSet(meviewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer
