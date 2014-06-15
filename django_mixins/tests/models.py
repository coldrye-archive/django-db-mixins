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

from django_mixins import *

class SignalHandlerTestMixin(MixinBase):

    field = fields.TextField(default = None, null = True)

    @classmethod
    def _preDelete(cls, model, instance=None, using=None, **extraargs):

        pass

    @classmethod
    def _postDelete(cls, model, instance=None, using=None, **extraargs):

        pass

    @classmethod
    def _preSave(cls, model, instance=None, raw=False, using=None, update_fields=None, **extraargs):

        pass

    @classmethod
    def _postSave(cls, model, instance=None, created=False, raw=False, using=None, update_fields=None, **extraargs):

        pass


class SignalHandlerTestModel(ModelBase, SignalHandlerTestMixin):

    pass


class CreationMixinTestModel(ModelBase, CreationMixin):

    pass


class ModificationMixinTestModel(ModelBase, ModificationMixin):

    field = fields.TextField(default = None, null = True)


class SystemDefinableMixinTestModel(ModelBase, SystemDefinableMixin):

    field = fields.TextField(default = None, null = True)

