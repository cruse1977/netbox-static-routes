import strawberry_django
from .. import filtersets, models
from netbox.graphql.filter_mixins import autotype_decorator, BaseFilterMixin

__all__ = (
    'StaticRouteFilter'
)


@strawberry_django.filter(models.StaticRoute, lookups=True)
@autotype_decorator(filtersets.StaticRouteFilterSet)
class StaticRouteFilter(BaseFilterMixin):
    pass
