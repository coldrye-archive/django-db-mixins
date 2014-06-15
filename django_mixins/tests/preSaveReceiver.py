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
from django.db.models.signals import pre_save

from django_mixins import MixinBase, ModelBase


class PreSaveReveicerTests(TestCase):

    def test_receiver_must_provide_args(self):

        class DummyMixinWithFieldsPreSave(MixinBase):

            instance = None
            raw = None
            using = None
            update_fields = None

            field_a = fields.TextField()
            field_b = fields.TextField()

            @classmethod
            def _preSave(cls, model, instance=None, raw=False, using=None, update_fields=None, **extraargs):

                instance.instance = instance
                instance.raw = raw
                instance.using = using
                instance.update_fields = update_fields

        class MockedWithFieldsPreSave(ModelBase, DummyMixinWithFieldsPreSave):

            def save(self, force_insert=False, force_update=False, using=None,
                     update_fields=None):

                pre_save.send(sender=MockedWithFieldsPreSave, instance=self, raw=False, using=using, update_fields=update_fields)

        args = (1, 'a')
        kwargs = {'field_b' : 'b'}

        m = MockedWithFieldsPreSave(*args, **kwargs)
        raw = False
        using = object()
        update_fields=['field_a']
        m.save(using=using, update_fields=update_fields)
        self.assertEqual(m.instance, m, msg = '_preSave should have provided instance.') 
        self.assertEqual(m.raw, raw, msg = '_preSave should have provided raw.') 
        self.assertEqual(m.using, using, msg = '_preSave should have provided using.') 
        self.assertListEqual(m.update_fields, update_fields, msg = '_preSave should have provided update_fields.') 

