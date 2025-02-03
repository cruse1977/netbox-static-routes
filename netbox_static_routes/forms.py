from dcim.models import Site, Device, Interface
from ipam.models import Prefix, VRF
from virtualization.models import VirtualMachine
from django import forms
from django.utils.translation import gettext_lazy as _
from utilities.forms.rendering import FieldSet, InlineFields
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm
from .models import StaticRoute
from utilities.forms.fields import (
    CommentField, DynamicModelChoiceField, ContentTypeChoiceField
)
from utilities.forms.widgets import HTMXSelect
from django.contrib.contenttypes.models import ContentType
from .constants import (
    STATICROUTE_SCOPE_TYPES,
    STATICROUTE_INT_SCOPE_TYPES
)
from utilities.forms.utils import get_field_value
from utilities.templatetags.builtins.filters import bettertitle

class StaticRouteForm(NetBoxModelForm):
    site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=False
    )
    scope_type = ContentTypeChoiceField(
        queryset=ContentType.objects.filter(model__in=STATICROUTE_SCOPE_TYPES),
        widget=HTMXSelect(),
        required=False,
        label=_('Scope type')
    )
    scope = DynamicModelChoiceField(
        label=_('Scope'),
        queryset=Device.objects.none(),  # Initial queryset
        required=False,
        disabled=True,
        selector=True
    )
    nh_int_scope_type = ContentTypeChoiceField(
        queryset=ContentType.objects.filter(model__in=STATICROUTE_INT_SCOPE_TYPES),
        widget=HTMXSelect(),
        required=False,
        label=_('Next Hop Interface Scope')
    )
    nh_int_scope = DynamicModelChoiceField(
        label=_('Scope'),
        queryset=Interface.objects.none(),  # Initial queryset
        required=False,
        disabled=True,
        selector=True
    )

    vrf = DynamicModelChoiceField(
        queryset=VRF.objects.all(),
        required=False
    )
    # need to be able to handle no VRF
    destination_prefix = DynamicModelChoiceField(
        queryset=Prefix.objects.all(),
        query_params={
            'vrf_id': '$vrf'
        }
    )

    bfd = forms.BooleanField(
        required=False,
        label="Bi-Directional Forwarding Detection"
    )
    comments = CommentField()

    fieldsets = (
        FieldSet('scope_type', 'scope', name=_('Scope')),
        FieldSet('destination_prefix', name=None),
        FieldSet('vrf', name=None),
        FieldSet('next_hop_ip', 'nh_int_scope_type', 'nh_int_scope', name=_('Next Hops')),
        FieldSet(
            'bfd',
            InlineFields('metric', 'distance'), name=_('Attributes'))
    )

    class Meta:
        model = StaticRoute
        fields = ('site', 'scope_type', 'nh_int_scope_type', 'vrf', 'destination_prefix', 'next_hop_ip', 'distance', 'metric', 'bfd', 'comments', 'tags')

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        initial = kwargs.get('initial', {})

        if instance is not None and instance.scope:
            initial['scope'] = instance.scope
            kwargs['initial'] = initial
        if instance is not None and instance.nh_int_scope:
            initial['nh_int_scope'] = instance.nh_int_scope

        super().__init__(*args, **kwargs)

        if scope_type_id := get_field_value(self, 'scope_type'):
            try:
                scope_type = ContentType.objects.get(pk=scope_type_id)
                model = scope_type.model_class()
                self.fields['scope'].queryset = model.objects.all()
                self.fields['scope'].widget.attrs['selector'] = model._meta.label_lower
                self.fields['scope'].disabled = False
                self.fields['scope'].label = _(bettertitle(model._meta.verbose_name))
            except ObjectDoesNotExist:
                pass

            if self.instance and scope_type_id != self.instance.scope_type_id:
                self.initial['scope'] = None
        if nh_int_scope_type_id := get_field_value(self, 'nh_int_scope_type'):
            try:
                nh_int_scope_type = ContentType.objects.get(pk=nh_int_scope_type_id)
                model = nh_int_scope_type.model_class()
                self.fields['nh_int_scope'].queryset = model.objects.all()
                self.fields['nh_int_scope'].widget.attrs['selector'] = model._meta.label_lower
                self.fields['nh_int_scope'].disabled = False
                self.fields['nh_int_scope'].label = _(bettertitle(model._meta.verbose_name))
            except ObjectDoesNotExist:
                pass

            if self.instance and nh_int_scope_type_id != self.instance.nh_int_scope_type_id:
                self.initial['nh_int_scope'] = None


    def clean(self):
        super().clean()

        # Assign the selected scope (if any)
        self.instance.scope = self.cleaned_data.get('scope')
        self.instance.nh_int_scope = self.cleaned_data.get('nh_int_scope')


class StaticRouteFilterForm(NetBoxModelFilterSetForm):
    model = StaticRoute
    static_route = forms.ModelMultipleChoiceField(
        queryset=StaticRoute.objects.all(),
        required=False
    )
    site = forms.ModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False
    )
    vrf = forms.ModelMultipleChoiceField(
        queryset=VRF.objects.all(),
        required=False
    )
    destination_prefix = forms.ModelMultipleChoiceField(
        queryset=Prefix.objects.all(),
        required=False
    )


