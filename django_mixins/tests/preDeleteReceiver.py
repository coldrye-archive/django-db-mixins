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
from django.db.models.signals import pre_delete

from django_mixins import MixinBase, ModelBase


class PreDeleteReveicerTests(TestCase):

    def test_receiver_must_provide_args(self):

        class DummyMixinWithFieldsPreDelete(MixinBase):

            instance = None
            using = None

            field_a = fields.TextField()
            field_b = fields.TextField()

            @classmethod
            def _preDelete(cls, model, instance=None, using=None, **extraargs):

                instance.instance = instance
                instance.using = using

        class MockedWithFieldsPreDelete(ModelBase, DummyMixinWithFieldsPreDelete):

            def delete(self, using=None):

                pre_delete.send(sender=MockedWithFieldsPreDelete, instance=self, using=using)

        args = (1, 'a')
        kwargs = {'field_b' : 'b'}

        m = MockedWithFieldsPreDelete(*args, **kwargs)
        using = object()
        m.delete(using=using)
        self.assertEqual(m.instance, m, msg = '_preDelete should have provided instance.') 
        self.assertEqual(m.using, using, msg = '_preDelete should have provided using.') 

