from django.urls import path, include
from utilities.urls import get_model_urls
from netbox.views.generic import ObjectChangeLogView
from . import views

urlpatterns = (
    path('static-routes/', include(get_model_urls('netbox_static_routes', 'staticroute', detail=False))),
    path('static-routes/<int:pk>', include(get_model_urls('netbox_static_routes', 'staticroute')))
)
