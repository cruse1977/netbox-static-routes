from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, F, OuterRef, Q, Subquery, Value
from django.db.models.expressions import RawSQL
from django.db.models.functions import Round
from dcim.models import Device
from utilities.query import count_related
from utilities.querysets import RestrictedQuerySet

class StaticRouteQuerySet(RestrictedQuerySet):

    def get_for_device(self, device):
        """
        Return all Static Routes on the Specified Device
        """
        from .models import StaticRoute
        q = Q()
        q |= Q(
            scope_type=ContentType.objects.get_by_natural_key('dcim', 'device'),
            scope_id=device.pk
        )

        return self.filter(q)
