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


from django.test import TestCase
from django.db.models import fields

from django_mixins import MixinBase, ModelBase


class PostInitReveicerTests(TestCase):

    def test_receiver_must_provide_args(self):

        class DummyMixinWithFieldsPostInit(MixinBase):

            instance = None

            field_a = fields.TextField()
            field_b = fields.TextField()

            @classmethod
            def _postInit(cls, model, instance=None, **extraargs):

                instance.instance = instance

        class MockedWithFieldsPostInit(ModelBase, DummyMixinWithFieldsPostInit):

            pass

        args = (1, 'a')
        kwargs = {'field_b' : 'b'}

        m = MockedWithFieldsPostInit(*args, **kwargs)
        self.assertEqual(m.instance, m, msg = '_postInit should have provided instance.') 

