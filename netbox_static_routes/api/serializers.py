from rest_framework import serializers
from ipam.api.serializers import PrefixSerializer
from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from ..models import StaticRoute

class StaticRouteSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_static_routes-api:staticroute-detail'
    )

    class Meta:
        model = StaticRoute
        fields = (
            'id', 'url', 'display', 'destination_prefix', 'next_hop', 'site', 'device', 'vrf', 'comments', 'tags', 'custom_fields', 'created', 'last_updated'
        )
        brief_fields = ('display', 'id', 'url')
