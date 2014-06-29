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
from django.utils import timezone
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

    def test_must_not_set_modification_fields_on_initial_save(self):

        # we will ignore timezone related warnings here
        with warnings.catch_warnings():

            warnings.simplefilter('ignore')

            m = ModificationMixinTestModel()
            m.save()

            self.assertIsNone(m.modifiedBy, msg = 'modifiedBy should not have been set.')
            self.assertIsNone(m.modifiedWhen, msg = 'modifiedWhen should not have been set.')

    def test_must_set_modification_fields_on_subsequent_save(self):

        # we will ignore timezone related warnings here
        with warnings.catch_warnings():

            warnings.simplefilter('ignore')

            m = ModificationMixinTestModel()
            m.save()
            m.field = 'a'
            m.save()

            self.assertEquals(m.modifiedBy, AnonymousUser().username, msg = 'modifiedBy should be the anonymous user.')
            self.assertIsNotNone(m.modifiedWhen, msg = 'modifiedWhen should have been set.')
            self.assertIsInstance(m.modifiedWhen, datetime.datetime, msg = 'modifiedWhen should have been an instance of datetime.')

    @skipIf(settings.USE_TZ==False, 'timezone support disabled')
    def test_must_not_cause_warnings_on_enabled_timezone_support(self):

        with warnings.catch_warnings(record=True) as w:

            warnings.simplefilter('always')

            m = ModificationMixinTestModel()
            m.save()

            if len(w) == 1:

                self.fail(w[0])

    @skipIf(settings.USE_TZ==False, 'timezone support disabled')
    def test_must_use_aware(self):

        m = ModificationMixinTestModel()
        m.save()
        m.field = 'a'
        m.save()

        self.assertTrue(timezone.is_aware(m.modifiedWhen), msg = 'modifiedWhen should have been timezone aware')

