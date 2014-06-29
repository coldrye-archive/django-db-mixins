# -*- coding: utf-8 -*-

#
#  Copyright 2014 Carsten Klein <trancesilken@gmail.com> 
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#


from django.db.models import fields
from django.utils import timezone

from .auth import CurrentUser
from .base import MixinBase
from .utils import set_once


class CreationMixin(MixinBase):

    createdBy = fields.TextField(default = None)
    createdWhen = fields.DateTimeField(default = None, null = False,
                                       auto_now = False, auto_now_add = True)

    @classmethod
    def _postInit(cls, model, instance=None, args=[],
                  kwargs={}, **extraargs):

        instance._createdBy = instance.__dict__['createdBy']
        delattr(instance, 'createdBy')
        instance.createdBy = set_once('createdBy');

        instance._createdWhen = instance.__dict__['createdWhen']
        delattr(instance, 'createdWhen')
        instance.createdWhen = set_once('createdWhen')

    @classmethod
    def _preSave(cls, model, instance=None, raw=False, using=None,
                 update_fields=None, **extraargs):

        if instance.createdBy is None:

            instance.createdBy = CurrentUser.username

        # createdWhen will be set automatically


# TODO: time zone support
class ModificationMixin(MixinBase):

    modifiedBy = fields.TextField(default = None, null = True)

    # we cannot rely on auto_now as it gets called for newly added
    # models as well, making any differentiation between auto_now_add 
    # and auto_now moot -> this seems to be an issue in Django's
    # DateTimeField#pre_save
    modifiedWhen = fields.DateTimeField(default = None, null = True,
                                        auto_now = False, auto_now_add = False)

    @classmethod
    def _postInit(cls, model, instance=None, args=tuple(),
                  kwargs={}, **extraargs):

        if instance.modifiedBy is None and instance.modifiedWhen is not None:

            instance.modifiedBy = CurrentUser.username

    @classmethod
    def _preSave(cls, model, instance=None, raw=False, using=None,
                 update_fields=None, **extraargs):

        # assume that the instance exists if pk is set
        # FIXME:does not work with pk mapped to attribute other than 'id'
        # FIXME:should check db if pk exists
        #pk = instance._meta.pk
        if instance.id is not None:

            instance.modifiedBy = CurrentUser.username
            instance.modifiedWhen = timezone.now()

