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


import datetime
import warnings

from django.test import TestCase
from django.utils.unittest import skipIf
from django.conf import settings
from django.contrib.auth.models import AnonymousUser

from django_mixins import MixinBase

from .models import ModificationMixinTestModel


class ModificationMixinTests(TestCase):

    def test_must_not_set_any_modification_field_on_init_when_missing(self):

        m = ModificationMixinTestModel()
        self.assertIsNone(m.modifiedBy, msg = 'modifiedBy should not have been set.')
        self.assertIsNone(m.modifiedWhen, msg = 'modifiedWhen should not have been set.')

    def test_must_set_modifiedBy_on_init_when_missing_and_modifiedWhen_is_available(self):

        modifiedWhen = datetime.datetime.now()
        m = ModificationMixinTestModel(1, modifiedWhen=modifiedWhen)
        self.assertEquals(m.modifiedBy, AnonymousUser().username, msg = 'modifiedBy should be the anonymous user.')
        self.assertEquals(m.modifiedWhen, modifiedWhen, msg = 'modifiedWhen should have been set to the specified value.')
        self.assertIsInstance(m.modifiedWhen, datetime.datetime, msg = 'modifiedWhen should have been an instance of datetime.')

    def test_must_set_modifiedBy_on_init_when_none_and_modifiedWhen_is_available(self):

        modifiedWhen = datetime.datetime.now()
        m = ModificationMixinTestModel(1, None, modifiedWhen=modifiedWhen)
        self.assertEquals(m.modifiedBy, AnonymousUser().username, msg = 'modifiedBy should be the anonymous user.')
        self.assertEquals(m.modifiedWhen, modifiedWhen, msg = 'modifiedWhen should have been set to the specified value.')
        self.assertIsInstance(m.modifiedWhen, datetime.datetime, msg = 'modifiedWhen should have been an instance of datetime.')

    def test_must_set_modifiedWhen_on_init_when_missing_and_modifiedBy_is_available(self):

        m = ModificationMixinTestModel(1, AnonymousUser().username)
        self.assertEquals(m.modifiedBy, AnonymousUser().username, msg = 'modifiedBy should be the anonymous user.')
        self.assertIsNotNone(m.modifiedWhen, msg = 'modifiedWhen should have been set.')
        self.assertIsInstance(m.modifiedWhen, datetime.datetime, msg = 'modifiedWhen should have been an instance of datetime.')

    def test_must_set_modifiedWhen_on_init_when_none_and_modifiedBy_is_available(self):

        m = ModificationMixinTestModel(1, AnonymousUser().username, None)
        self.assertEquals(m.modifiedBy, AnonymousUser().username, msg = 'modifiedBy should be the anonymous user.')
        self.assertIsNotNone(m.modifiedWhen, msg = 'modifiedWhen should have been set.')
        self.assertIsInstance(m.modifiedWhen, datetime.datetime, msg = 'modifiedWhen should have been an instance of datetime.')

    def test_must_not_set_modification_fields_on_initial_save(self):

        m = ModificationMixinTestModel()
        m.save()
        self.assertIsNone(m.modifiedBy, msg = 'modifiedBy should not have been set.')
        self.assertIsNone(m.modifiedWhen, msg = 'modifiedWhen should not have been set.')

    def test_must_set_modification_fields_on_save(self):

        m = ModificationMixinTestModel()
        m.save()
        m.field = 'a'

        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            m.save()

        self.assertEquals(m.modifiedBy, AnonymousUser().username, msg = 'modifiedBy should be the anonymous user.')
        self.assertIsNotNone(m.modifiedWhen, msg = 'modifiedWhen should have been set.')
        self.assertIsInstance(m.modifiedWhen, datetime.datetime, msg = 'modifiedWhen should have been an instance of datetime.')

    @skipIf(settings.USE_TZ==False, 'timezone support disabled')
    def test_timezone_support(self):

        m = ModificationMixinTestModel()
        m.save()
        m.field = 'a'

        if settings.USE_TZ:

            with warnings.catch_warnings(record=True) as w:

                warnings.simplefilter('always')
                m.save()
                if len(w) == 1:

                    self.fail(w[0])

