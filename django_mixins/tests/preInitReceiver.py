
from django.test import TestCase
from django.db.models import fields

from django_mixins import MixinBase, ModelBase


class PreInitReveicerTests(TestCase):

    def test_receiver_must_provide_args(self):

        class DummyMixinWithFieldsPreInit(MixinBase):

            field_a = fields.TextField()
            field_b = fields.TextField()

            @classmethod
            def _preInit(cls, model, args=[], kwargs={}, **extraargs):

                pass

        class MockedWithFieldsPreInit(ModelBase, DummyMixinWithFieldsPreInit):

            pass

        args = (1, 'a')
        kwargs = {'field_b' : 'b'}

        m = MockedWithFieldsPreInit(*args, **kwargs)
        self.assertEqual(m.id, args[0], msg = '_preInit should have provided args:id.')
        self.assertEqual(m.field_a, args[1], msg = '_preInit should have provided args:field_a.')
        self.assertEqual(m.field_b, kwargs.values()[0], msg = '_preInit should have provided kwargs:field_b.')

