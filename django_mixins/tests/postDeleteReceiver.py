
from django.test import TestCase
from django.db.models import fields
from django.db.models.signals import post_delete

from django_mixins import MixinBase, ModelBase


class PostDeleteReveicerTests(TestCase):

    def test_receiver_must_provide_args(self):

        class DummyMixinWithFieldsPostDelete(MixinBase):

            instance = None
            using = None

            field_a = fields.TextField()
            field_b = fields.TextField()

            @classmethod
            def _postDelete(cls, model, instance=None, using=None, **extraargs):

                instance.instance = instance
                instance.using = using

        class MockedWithFieldsPostDelete(ModelBase, DummyMixinWithFieldsPostDelete):

            def delete(self, using=None):

                post_delete.send(sender=MockedWithFieldsPostDelete, instance=self, using=using)

        args = (1, 'a')
        kwargs = {'field_b' : 'b'}

        m = MockedWithFieldsPostDelete(*args, **kwargs)
        using=object()
        m.delete(using=using)
        self.assertEqual(m.instance, m, msg = '_postDelete should have provided instance.') 
        self.assertEqual(m.using, using, msg = '_postDelete should have provided using.') 

