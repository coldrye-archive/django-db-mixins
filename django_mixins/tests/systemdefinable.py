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

