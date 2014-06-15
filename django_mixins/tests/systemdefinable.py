

import datetime

from django.test import TestCase

from django.contrib.auth.models import AnonymousUser

from .models import SystemDefinableMixinTestModel


class SystemDefinableMixinTests(TestCase):

    def test_must_not_prevent_save_if_system_flag_is_set_on_initial_save(self):

        self.fail()

    def test_must_prevent_modification_of_system_flag_if_set(self):

        self.fail()

    def test_must_prevent_save_if_system_flag_is_set(self):

        self.fail()

        #m = SystemDefinableMixinTestModel()

