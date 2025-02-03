#from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField
from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet
from .constants import (
    STATICROUTE_SCOPE_TYPES,
    STATICROUTE_INT_SCOPE_TYPES
)
from django.db.models import Q
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from .querysets import StaticRouteQuerySet
'''
class CommonStaticRoute(NetBoxModel):
   
    devices = models.ManyToManyField(
        to='dcim.Device',
        related_name='common_static_routes',
        blank=True
    )

    virtual_machines = models.ManyToManyField(
        to='virtualization.VirtualMachine',
        related_name='common_static_routes',
        blank=True
    )


    site = models.ForeignKey(
        to='dcim.Site',
        on_delete=models.PROTECT,
        related_name="%(class)s_related",
        blank=True,
        null=True
    )

    vrf = models.ForeignKey(
        to='ipam.VRF',
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True,
        verbose_name='VRF'
    )
    destination_prefix = models.ForeignKey(
        to='ipam.Prefix',
        on_delete=models.PROTECT,
        null=True
    )
    next_hop_ip = ArrayField(
        base_field=models.GenericIPAddressField(),
        null=True
    )

    next_hop_str = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    metric = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(65535)
        ],
        verbose_name='Metric',
        blank=True,
        null=True
    )

    distance = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(255)
        ],
        verbose_name='Administrative distance',
        blank=True,
        null=True
    )

    bfd = models.BooleanField(
        default=False,
        verbose_name="Bi-Directional Forwarding Detection"
    )
    comments = models.TextField(
        blank=True
    )

    openconfig_json = models.JSONField(
        default = dict,
        blank = True,
        null = True
    )

    class Meta:
        verbose_name_plural = 'Common Static Routes'
            
    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_static_routes:commonstaticroute', args=[self.pk])

'''

class StaticRoute(NetBoxModel):

    site = models.ForeignKey(
        to='dcim.Site',
        on_delete=models.PROTECT,
        related_name="%(class)s_related",
        blank=True,
        null=True
    )

    scope_type = models.ForeignKey(
        to='contenttypes.ContentType',
        on_delete=models.CASCADE,
        limit_choices_to=Q(model__in=STATICROUTE_SCOPE_TYPES),
        blank=True,
        null=True
    )
    scope_id = models.PositiveBigIntegerField(
        blank=True,
        null=True
    )
    scope = GenericForeignKey(
        ct_field='scope_type',
        fk_field='scope_id'
    )

    vrf = models.ForeignKey(
        to='ipam.VRF',
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True,
        verbose_name='VRF'
    )
    destination_prefix = models.ForeignKey(
        to='ipam.Prefix',
        on_delete=models.PROTECT,
        null=True
    )
    next_hop_ip = ArrayField(
        base_field=models.GenericIPAddressField(),
        null=True
    )

    nh_int_scope_type = models.ForeignKey(
        to='contenttypes.ContentType',
        related_name='+',
        on_delete=models.CASCADE,
        limit_choices_to=Q(model__in=STATICROUTE_INT_SCOPE_TYPES),
        blank=True,
        null=True
    )

    nh_int_scope_id = models.PositiveBigIntegerField(
        blank=True,
        null=True
    )
    nh_int_scope = GenericForeignKey(
        ct_field='nh_int_scope_type',
        fk_field='nh_int_scope_id'
    )

    metric = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(65535)
        ],
        verbose_name='Metric',
        blank=True,
        null=True
    )

    distance = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(255)
        ],
        verbose_name='Administrative distance',
        blank=True,
        null=True
    )

    bfd = models.BooleanField(
        default=False,
        verbose_name="Bi-Directional Forwarding Detection"
    )
    comments = models.TextField(
        blank=True
    )

    openconfig_json = models.JSONField(
        default = dict,
        blank = True,
        null = True
    )
    objects = StaticRouteQuerySet.as_manager()

    def save(self, *args, **kwargs):
        ''' todo: add validation for vmint and int to vm and device '''
        super(StaticRoute, self).save( *args, **kwargs)
        #super(StaticRoute, self).save(update_fields=['openconfig_json'])


    class Meta:
        verbose_name_plural = 'Static Routes'
        indexes = (
            models.Index(fields=('scope_type', 'scope_id')),
            models.Index(fields=('nh_int_scope_type', 'nh_int_scope_id')),          
        )

        #ordering = ('scope', 'vrf', 'destination_prefix', 'next_hop')
        #unique_together = ['scope', 'vrf', 'destination_prefix']

            

    def __str__(self):
        if self.vrf:
            return f'{self.scope}:{self.vrf}:{self.destination_prefix}'
        else: 
            return f'{self.scope}:{self.destination_prefix}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_static_routes:staticroute', args=[self.pk])
