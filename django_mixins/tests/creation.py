

import datetime
import warnings

from django.db.models import Model
from django.conf import settings
from django.test import TestCase
from django.utils.unittest import skipIf
from django.contrib.auth.models import AnonymousUser

from django_mixins import MixinBase, CreationMixin

from .models import CreationMixinTestModel


class CreationMixinTests(TestCase):

    def test_must_set_both_creation_fields_on_init_when_missing(self):

        m = CreationMixinTestModel()
        self.assertEquals(m.createdBy, AnonymousUser().username, msg = 'createdBy should be the anonymous user.')
        self.assertIsNotNone(m.createdWhen, msg = 'createdWhen should have been set.')
        self.assertIsInstance(m.createdWhen, datetime.datetime, msg = 'createdWhen should have been an instance of datetime.')

    def test_must_set_createdBy_on_init_when_missing(self):

        createdWhen = datetime.datetime.now()
        m = CreationMixinTestModel(1, createdWhen=createdWhen)
        self.assertEquals(m.createdBy, AnonymousUser().username, msg = 'createdBy should be the anonymous user.')
        self.assertEquals(m.createdWhen, createdWhen, msg = 'createdWhen should have been set to the specified value.')
        self.assertIsInstance(m.createdWhen, datetime.datetime, msg = 'createdWhen should have been an instance of datetime.')

    def test_must_set_createdBy_on_init_when_none(self):

        createdWhen = datetime.datetime.now()
        m = CreationMixinTestModel(1, None, createdWhen=createdWhen)
        self.assertEquals(m.createdBy, AnonymousUser().username, msg = 'createdBy should be the anonymous user.')
        self.assertEquals(m.createdWhen, createdWhen, msg = 'createdWhen should have been set to the specified value.')
        self.assertIsInstance(m.createdWhen, datetime.datetime, msg = 'createdWhen should have been an instance of datetime.')

    def test_must_set_createdWhen_on_init_when_missing(self):

        m = CreationMixinTestModel(1, AnonymousUser().username)
        self.assertEquals(m.createdBy, AnonymousUser().username, msg = 'createdBy should be the anonymous user.')
        self.assertIsNotNone(m.createdWhen, msg = 'createdWhen should have been set.')
        self.assertIsInstance(m.createdWhen, datetime.datetime, msg = 'createdWhen should have been an instance of datetime.')

    def test_must_set_createdWhen_on_init_when_none(self):

        m = CreationMixinTestModel(1, AnonymousUser().username, None)
        self.assertEquals(m.createdBy, AnonymousUser().username, msg = 'createdBy should be the anonymous user.')
        self.assertIsNotNone(m.createdWhen, msg = 'createdWhen should have been set.')
        self.assertIsInstance(m.createdWhen, datetime.datetime, msg = 'createdWhen should have been an instance of datetime.')

    @skipIf(settings.USE_TZ==False, 'timezone support disabled')
    def test_timezone_support(self):

        m = CreationMixinTestModel()

        if settings.USE_TZ:

            with warnings.catch_warnings(record=True) as w:

                warnings.simplefilter('always')
                m.save()
                if len(w) == 1:

                    self.fail(w[0])

