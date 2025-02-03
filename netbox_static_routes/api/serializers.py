from django.contrib.contenttypes.models import ContentType
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from ipam.api.serializers import PrefixSerializer
from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from netbox.api.fields import ContentTypeField
from ..models import StaticRoute
from ..constants import *
from utilities.api import get_serializer_for_model
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

class StaticRouteSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_static_routes-api:staticroute-detail'
    )

    scope_type = ContentTypeField(
        queryset=ContentType.objects.filter(
            model__in=STATICROUTE_SCOPE_TYPES
        ),
        allow_null=True,
        required=False,
        default=None
    )
    scope_id = serializers.IntegerField(allow_null=True, required=False, default=None)
    scope = serializers.SerializerMethodField(read_only=True)

    nh_int_scope_type = ContentTypeField(
        queryset=ContentType.objects.filter(
            model__in=STATICROUTE_INT_SCOPE_TYPES
        ),
        allow_null=True,
        required=False,
        default=None
    )
    nh_int_scope_id = serializers.IntegerField(allow_null=True, required=False, default=None)
    nh_int_scope = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StaticRoute
        fields = (
            'id',
            'url',
            'display',
            'destination_prefix',
            'next_hop_ip',
            'scope',
            'scope_type',
            'scope_id',
            'nh_int_scope',
            'nh_int_scope_type',
            'nh_int_scope_id',
            'site',
            'vrf',
            'bfd',
            'metric',
            'distance',
            'comments',
            'tags',
            'custom_fields',
            'created',
            'last_updated'
        )
        brief_fields = ('display', 'id', 'url', 'scope', 'destination_prefix')

    @extend_schema_field(serializers.JSONField(allow_null=True))
    def get_scope(self, obj):
        if obj.scope_id is None:
            return None
        serializer = get_serializer_for_model(obj.scope)
        context = {'request': self.context['request']}
        return serializer(obj.scope, nested=True, context=context).data

    @extend_schema_field(serializers.JSONField(allow_null=True))
    def get_nh_int_scope(self, obj):
        if obj.nh_int_scope_id is None:
            return None
        serializer = get_serializer_for_model(obj.nh_int_scope)
        context = {'request': self.context['request']}
        return serializer(obj.nh_int_scope, nested=True, context=context).data

    @extend_schema_field(OpenApiTypes.STR)
    def get_for_device(self, queryset, name, value):
        return queryset.get_for_device(value)