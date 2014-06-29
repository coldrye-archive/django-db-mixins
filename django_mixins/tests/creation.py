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

import warnings

from django.db.models import Model
from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from django.utils.unittest import skipIf
from django.contrib.auth.models import AnonymousUser

from django_mixins import MixinBase, CreationMixin

from .models import CreationMixinTestModel


class CreationMixinTests(TestCase):

    def test_must_not_set_any_creation_field_on_init_when_missing(self):

        m = CreationMixinTestModel()
        self.assertIsNone(m.createdBy, msg = 'createdBy should not have been set.')
        self.assertIsNone(m.createdWhen, msg = 'createdWhen should not have been set.')

    def test_must_make_createdBy_a_set_once_field_on_init(self):

        m = CreationMixinTestModel()
        m.createdBy = AnonymousUser().username
        def callable():

            m.createdBy = None

        self.assertRaises(AttributeError, callable)

    def test_must_make_createdWhen_a_set_once_field_on_init(self):

        m = CreationMixinTestModel()
        m.createdWhen = timezone.now()
        def callable():

            m.createdWhen = None

        self.assertRaises(AttributeError, callable)

    def test_must_set_createdBy_on_save(self):

        m = CreationMixinTestModel()
        m.save()

        self.assertEquals(m.createdBy, AnonymousUser().username)

    def test_must_not_modify_createdBy_on_save(self):

        m = CreationMixinTestModel()
        m.createdBy = 'test'
        m.save()

        self.assertEquals(m.createdBy, 'test')

    def test_must_set_createdWhen_on_save(self):

        m = CreationMixinTestModel()
        m.save()

        self.assertIsNotNone(m.createdWhen)

    def test_save_must_raise_on_manual_set_of_createdWhen(self):

        m = CreationMixinTestModel()
        nowdt = timezone.now()
        m.createdWhen = nowdt
        self.assertRaises(AttributeError, m.save)

    @skipIf(settings.USE_TZ==False, 'timezone support disabled')
    def test_must_not_cause_warnings_on_enabled_timezone_support(self):

        with warnings.catch_warnings(record=True) as w:

            warnings.simplefilter('always')

            m = CreationMixinTestModel()
            m.save()

            if len(w) == 1:

                self.fail(w[0])

    @skipIf(settings.USE_TZ==False, 'timezone support disabled')
    def test_must_use_aware(self):

        m = CreationMixinTestModel()
        m.save()

        self.assertTrue(timezone.is_aware(m.createdWhen), msg = 'createdWhen should have been timezone aware')

