import strawberry
import strawberry_django
from .types import StaticRouteType
from ..models import StaticRoute
from typing import List

@strawberry.type(name="Query")
class NetBoxStaticRoutesQuery:
    """
    Defines the queries available to this plugin via the graphql api.
    """
    static_route: StaticRouteType = strawberry_django.field()
    static_route_list: List[StaticRouteType] = strawberry_django.field()
