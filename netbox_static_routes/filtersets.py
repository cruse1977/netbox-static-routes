from netbox.filtersets import NetBoxModelFilterSet
from .models import StaticRoute

class StaticRouteFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = StaticRoute
        fields = ('id', 'site', 'scope_id', 'vrf', 'destination_prefix')

    def search(self, queryset, name, value):
        return queryset.filter(description__icontains=value)
        