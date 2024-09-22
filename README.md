# netbox-static-routes
[Netbox](https://github.com/netbox-community/netbox) plugin for static route documentation.

Based upon the original repo: [jbparrish17/netbox-static-routes](https://github.com/jbparrish17/netbox-static-routes) modified for additional functionality and NetBox v4.1+ Support

## Installation
This project is not currently packaged. Installation will require cloning the repository and running setup.py in the Netbox virtual environment.

## Configuration

### Netbox Configuration
After running setup.py, enable the plugin in `netbox/netbox/configuration.py` in the `PLUGINS` parameter (which is a list):

```python
# configuration.py
PLUGINS = [
    'netbox_static_routes',
]
```

Save the file and restart the Netbox service.

### Apply Migrations
Like any Netbox plugin which implements database models, you must apply migration files included in the project using the `migrate` management command:

```bash
$ python netbox/manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, circuits, contenttypes, dcim, django_rq, extras, ipam, netbox_access_lists, sessions, social_django, taggit, tenancy, users, virtualization, wireless
Running migrations:
  Applying netbox_static_routes.0001_initial... OK
```

You may or may not have to restart the Netbox service after applying migrations.

Netbox Static Routes should be usable upon page refresh.

## Roadmap
### Next-Hop Types


## Contributing

