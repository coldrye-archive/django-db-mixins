
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

