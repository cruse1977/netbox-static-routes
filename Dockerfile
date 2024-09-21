ARG NETBOX_VARIANT=v4.1

FROM netboxcommunity/netbox:${NETBOX_VARIANT}

RUN mkdir -pv /plugins/netbox-static-routes
COPY . /plugins/netbox-static-routes

RUN /opt/netbox/venv/bin/python3 /plugins/netbox-static-routes/setup.py develop && \
    cp -rf /plugins/netbox-static-routes/netbox_static_routes/ /opt/netbox/venv/lib/python3.12/site-packages/netbox_static_routes