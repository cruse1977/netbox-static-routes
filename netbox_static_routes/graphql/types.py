
"""
Define the object types and queries availble via the graphql api.
"""

import strawberry
import strawberry_django


from typing import Annotated, List, Union
from .filters import StaticRouteFilter
from ..models import StaticRoute
from netbox.graphql.types import OrganizationalObjectType

@strawberry_django.type(
    StaticRoute,
    fields='__all__',
    filters=StaticRouteFilter
)

class StaticRouteType(OrganizationalObjectType):
    """
    Defines the object type for the django model StaticRoute
    """
    site: Annotated["SiteType", strawberry.lazy("dcim.graphql.types")] | None
    device: Annotated["DeviceType", strawberry.lazy("dcim.graphql.types")] | None
    destination_prefix: Annotated["PrefixType", strawberry.lazy("ipam.graphql.types")] | None
    vrf: Annotated["VRFType", strawberry.lazy("ipam.graphql.types")] | None

    class Meta:
        """
        Associates the filterset, fields, and model for the django model AccessList.
        """
        @strawberry_django.field
        def staticroutes(self) -> List[Annotated["StaticRoute", strawberry.lazy('staticroutes.graphql.types')]]:
            return self.staticroutes.all()
