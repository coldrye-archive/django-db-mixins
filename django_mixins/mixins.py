

import datetime

from django.db.models import fields

from .auth import CurrentUser
from .base import MixinBase
from .utils import set_once


# TODO: timezone support
class CreationMixin(MixinBase):

    createdBy = fields.TextField(default = None)
    createdWhen = fields.DateTimeField(default = None)

    @classmethod
    def _postInit(cls, model, instance=None, args=[], kwargs={}, **extraargs):

        instance._createdBy = instance.__dict__['createdBy']
        delattr(instance, 'createdBy')
        instance.createdBy = set_once('createdBy');

        if instance._createdBy is None:

            instance._createdBy = CurrentUser.username

        instance._createdWhen = instance.__dict__['createdWhen']
        delattr(instance, 'createdWhen')
        instance.createdWhen = set_once('createdWhen')

        if instance._createdWhen is None:

            instance._createdWhen = datetime.datetime.now() 


# TODO: time zone support
class ModificationMixin(MixinBase):

    modifiedBy = fields.TextField(default = None, null = True)
    modifiedWhen = fields.DateTimeField(default = None, null = True)

    @classmethod
    def _postInit(cls, model, instance=None, args=tuple(), kwargs={}, **extraargs):

        if instance.modifiedBy is not None and instance.modifiedWhen is None:

            instance.modifiedWhen = datetime.datetime.now()

        elif instance.modifiedBy is None and instance.modifiedWhen is not None:

            instance.modifiedBy = CurrentUser.username

    @classmethod
    def _preSave(cls, model, instance=None, raw=False, using=None, update_fields=None, **extraargs):

        # assume that the instance exists if pk is set
        # FIXME:does not work with pk mapped to attribute other than 'id'
        # FIXME:should check db if pk exists
        #pk = instance._meta.pk
        if instance.id is not None:

            instance.modifiedBy = CurrentUser.username
            instance.modifiedWhen = datetime.datetime.now()

