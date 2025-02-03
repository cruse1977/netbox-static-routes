from netbox.views import generic
from dcim.models import Device
from virtualization.models import VirtualMachine
from . import filtersets, forms, models, tables
from utilities.views import ViewTab, register_model_view
from django.shortcuts import render

class StaticRouteView(generic.ObjectView):
    queryset = models.StaticRoute.objects.all()

class StaticRouteListView(generic.ObjectListView):
    queryset = models.StaticRoute.objects.all()
    table = tables.StaticRouteTable
    filterset = filtersets.StaticRouteFilterSet
    filterset_form = forms.StaticRouteFilterForm

class StaticRouteEditView(generic.ObjectEditView):
    queryset = models.StaticRoute.objects.all()
    form = forms.StaticRouteForm

class StaticRouteDeleteView(generic.ObjectDeleteView):
    queryset = models.StaticRoute.objects.all()



class DeviceSRChildView(generic.ObjectChildrenView):
    child_model = models.StaticRoute
    table = tables.StaticRouteTable
    filterset = filtersets.StaticRouteFilterSet
    template_name= 'generic/object_children.html'


@register_model_view(Device, name='staticroutes', path='staticroutes')
class DeviceSRView(generic.ObjectChildrenView):
    queryset = Device.objects.all()
    child_model = models.StaticRoute
    table = tables.StaticRouteTable
    template_name= 'generic/object_children.html'
    tab = ViewTab(
        label='Static Routes',
        badge=lambda obj: models.StaticRoute.objects.get_for_device(obj).count(),
        permission='netbox_static_routes.view_static_routes'
    )

    def get_children(self, request, parent):
        return models.StaticRoute.objects.get_for_device(parent)
