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


import six

import django.db.models.base as djbase

from .utils import InstanceDescriptorMixin
from .auth import CurrentUser


class ModelBase(djbase.Model):

    class Meta:

        abstract = True


class MixinMeta(djbase.ModelBase):

    def __new__(cls, name, bases, attrs):

        # all mixins are abstract
        supernew = super(MixinMeta, cls).__new__

        class Meta:

            abstract = True

        attrs['Meta'] = Meta

        return supernew(cls, name, bases, attrs)


class MixinBase(djbase.Model, InstanceDescriptorMixin, six.with_metaclass(MixinMeta)):

    class Meta:

        abstract = True

