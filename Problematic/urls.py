from .api import ProblematicViewSet
from rest_framework_mongoengine import routers as merouters
from django.conf.urls import url
from .api_fichier import DatasetView, ModelTrainedView, ModelGeneratedView


merouter = merouters.DefaultRouter()
merouter.register(r'Problematics', ProblematicViewSet)

urlpatterns = [
    url(r'^Datafile/Datasets/$', DatasetView.as_view(), name='dataset-List'),
    url(r'^Datafile/Modeltraineds/$', ModelTrainedView.as_view(), name='ModelTrained-Create'),
    url(r'^Problematics/(?P<id>[^/.]+)/ModelTrained/(?P<idmodel>[^/.]+)/$', ModelGeneratedView.as_view())
]

urlpatterns += merouter.urls
