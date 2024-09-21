from netbox.plugins import PluginConfig
from .version import __version__

class NetBoxStaticRoutesConfig(PluginConfig):
    name = 'netbox_static_routes'
    verbose_name = 'Static Routes'
    description = 'Manage static routes in Netbox'
    version = __version__
    author = 'Chris Russell'
    author_email = 'cruse1977123@gmail.com'
    base_url = 'static-routes'
    required_settings = []
    min_version = '4.1.0'
    max_version = '4.1.20'
    default_settings = {}

config = NetBoxStaticRoutesConfig
