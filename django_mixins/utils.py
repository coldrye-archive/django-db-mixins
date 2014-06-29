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


from django.db.models.query_utils import DeferredAttribute

# based on blog.brianbeck.com/post/74086029/instance-descriptors
class InstanceDescriptorMixin(object):

    def __getattribute__(self, name):

        result = object.__getattribute__(self, name)
        if hasattr(result, '__get__'):

            result = result.__get__(self, self.__class__)

        return result

    def __setattr__(self, name, value):

        try:

            attrib = object.__getattribute__(self, name)

        except AttributeError:

            pass

        else:

            if (hasattr(attrib, '__set__')):

                return attrib.__set__(self, value)

        return object.__setattr__(self, name, value)


class set_once(object):

    _attrib = None

    def __init__(self, attrib):

        self._attrib = attrib

    def __get__(self, instance, cls=None):
        
        result = None
        if isinstance(self._attrib, str):

            attrib = '_' + self._attrib
            result = getattr(instance, attrib)

        elif hasattr(self._attrib, '__get__'):

            result = self._attrib.__get__(instance, cls)

        return result

    def __set__(self, instance, value):

        if isinstance(self._attrib, str):

            attrib = '_' + self._attrib
            if getattr(instance, attrib) is not None:

                raise AttributeError("property '%s' can be set once only." % self._attrib)

            result = setattr(instance, attrib, value)

        elif hasattr(self._attrib, '__set__'):

            result = self._attrib.__set__(instance, value)


class set_once_deferred(DeferredAttribute, set_once):

    pass

