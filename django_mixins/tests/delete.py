
import sys

from django.test import TestCase

from .models import SignalHandlerTestModel


class SignalHandlerTests(TestCase):

    def test_pre_save(self):

        m = SignalHandlerTestModel()
        m.field = 'a'
        m.save()

    def test_post_save(self):

        m = SignalHandlerTestModel()
        m.field = 'a'
        m.save()

