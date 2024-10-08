from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site
from ipam.models import Prefix
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from utilities.testing import APITestCase, APIViewTestCases

from netbox_static_routes.models import StaticRoute


class AppTest(APITestCase):
    def test_root(self):
        url = reverse("plugins-api:netbox_static_routes-api:api-root")
        response = self.client.get(f"{url}?format=api", **self.header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ACLTestCase(
    APIViewTestCases.APIViewTestCase,
):
    """Test the AccessList Test"""

    model = StaticRoute
    view_namespace = "plugins-api:netbox_static_routes"
    brief_fields = ["display", "id", "url"]

    @classmethod
    def setUpTestData(cls):
        site = Site.objects.create(name="Site 1", slug="site-1")
        manufacturer = Manufacturer.objects.create(
            name="Manufacturer 1",
            slug="manufacturer-1",
        )
        devicetype = DeviceType.objects.create(
            manufacturer=manufacturer,
            model="Device Type 1",
        )
        devicerole = DeviceRole.objects.create(
            name="Device Role 1",
            slug="device-role-1",
        )
        device = Device.objects.create(
            name="Device 1",
            site=site,
            device_type=devicetype,
            role=devicerole,
        )
        prefix_1 = Prefix.objects.create(
            prefix='10.1.1.0/24'
        )
        prefix_2 = Prefix.objects.create(
            prefix='10.2.2.0/24'
        )
        prefix_3 = Prefix.objects.create(
            prefix='10.3.3.0/24'
        )
        prefix_4 = Prefix.objects.create(
            prefix='10.4.4.0/24'
        )
        prefix_5 = Prefix.objects.create(
            prefix='10.5.5.0/24'
        )
        prefix_6 = Prefix.objects.create(
            prefix='10.6.6.0/24'
        )
        static_routes = (
            StaticRoute(
                site=site,
                device=device,
                destination_prefix=prefix_1
            ),
            StaticRoute(
                site=site,
                device=device,
                destination_prefix=prefix_5
            ),
            StaticRoute(
                site=site,
                device=device,
                destination_prefix=prefix_6
            ),
        )
        StaticRoute.objects.bulk_create(static_routes)

        cls.create_data = [
            {
                "site": site.id,
                "device": device.id,
                "destination_prefix": prefix_2.id,
                "vrf": None,
                "next_hop": ['10.1.1.1']
            },
            {
                "site": site.id,
                "device": device.id,
                "destination_prefix": prefix_3.id,
                "vrf": None,
                "next_hop": ['10.1.1.1']
            },
            {
                "site": site.id,
                "device": device.id,
                "destination_prefix": prefix_4.id,
                "vrf": None,
                "next_hop": ['10.1.1.1']
            }
        ]
