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


from django.db.models import Model
from django.test import TestCase

from django_mixins import MixinBase, ModelBase


class ClassPreparedReveicerTests(TestCase):

    def test_receiver_must_not_call(self):

        class MockedWithoutMixins(ModelBase):

            wasCalled = False

            @classmethod
            def _classPrepared(cls, model, **kwargs):

                model.wassCalled = True

        self.assertFalse(MockedWithoutMixins.wasCalled, msg = '_classPrepared should not have been called.')

    def test_receiver_must_call(self):

        class DummyMixinClassPrepared(MixinBase):

            wasCalled = False

            @classmethod
            def _classPrepared(cls, model, **kwargs):

                model.wasCalled = True

        class MockedWithMixinsClassPrepared(ModelBase, DummyMixinClassPrepared):

            pass

        self.assertTrue(MockedWithMixinsClassPrepared.wasCalled, msg = '_classPrepared should have been called.')

    def test_receiver_must_handle_inherited_mixins(self):

        class DummyMixinClassPrepared(MixinBase):

            wasCalled = False

            @classmethod
            def _classPrepared(cls, model, **kwargs):

                model.wasCalled = True

        class MockedWithMixinsClassPreparedBase(ModelBase, DummyMixinClassPrepared):

            pass

        class MockedWithInheritedMixinsClassPrepared(MockedWithMixinsClassPreparedBase):

            pass

        self.assertTrue(MockedWithInheritedMixinsClassPrepared.wasCalled, msg = '_classPrepared should have been called.')

    def test_receiver_must_not_prepare_abstract_models(self):

        class DummyMixinClassPrepared(MixinBase):

            wasCalled = False

            @classmethod
            def _classPrepared(cls, model, **kwargs):

                model.wasCalled = True

        class MockedAbstractWithMixinsClassPrepared(ModelBase, DummyMixinClassPrepared):

            class Meta:

                abstract = True

        self.assertFalse(MockedAbstractWithMixinsClassPrepared.wasCalled, msg = '_classPrepared should not have been called.')

    def test_mixinMeta_handlerMap_must_contain_single_handler(self):

        class DummyMixinWithSingleHandlerClassPrepared(MixinBase):

            @classmethod
            def _preInit(cls, model, args=tuple(), kwargs={}, **extraargs):

                pass

        class MockedWithMixinsWithSingleHandlerClassPrepared(ModelBase, DummyMixinWithSingleHandlerClassPrepared):

            pass

        meta = MockedWithMixinsWithSingleHandlerClassPrepared._mixinMeta
        expected = {'preDelete': None, 'postSave': None, 'postDelete': None, 'preSave': None, 
                    'preInit': [DummyMixinWithSingleHandlerClassPrepared._preInit], 'postInit': None}
        self.assertDictEqual(meta.handlerMap, expected, 'handlerMap should contain only the expected handlers.')

    def test_mixinMeta_handlerMap_must_contain_all_declared_handlers(self):

        class DummyMixinWithSingleHandlerPreInitClassPrepared(MixinBase):

            @classmethod
            def _preInit(cls, model, args=tuple(), kwargs={}, **extraargs):

                pass

        class DummyMixinWithSingleHandlerPostSaveClassPrepared(MixinBase):

            @classmethod
            def _postSave(cls, model, instance=None, raw=False, using=False, update_fields=None, **extraargs):

                pass

        class DummyMixinWithAllHandlersClassPrepared(DummyMixinWithSingleHandlerPreInitClassPrepared,
                                                     DummyMixinWithSingleHandlerPostSaveClassPrepared):

            @classmethod
            def _preInit(cls, model, args=tuple(), kwargs={}, **extraargs):

                pass

            @classmethod
            def _postInit(cls, model, instance=None, args=tuple(), kwargs={}, **extraargs):

                pass

            @classmethod
            def _preDelete(cls, model, instance=None, **extraargs):

                pass

            @classmethod
            def _postDelete(cls, model, instance=None, **extraargs):

                pass

            @classmethod
            def _preSave(cls, model, instance=None, raw=False, using=False, update_fields=None, **extraargs):

                pass

            @classmethod
            def _postSave(cls, model, instance=None, raw=False, using=False, update_fields=None, **extraargs):

                pass

        class DummyMixinWithSingleHandlerPostDeleteClassPrepared(MixinBase):

            @classmethod
            def _postDelete(cls, model, instance=None, **extraargs):

                pass

        class MockedWithMixinsBaseClassPrepared(ModelBase, DummyMixinWithAllHandlersClassPrepared,
                                                DummyMixinWithSingleHandlerPostDeleteClassPrepared):

            pass

        # note: we will not test for mixins being implemented/subclassed twice or more often
        # as the mro of the resulting model class will be normalized and contain each base
        # class only once

        class MockedWithMixinsWithAllHandlersClassPrepared(MockedWithMixinsBaseClassPrepared):

            pass

        meta = MockedWithMixinsWithAllHandlersClassPrepared._mixinMeta
        expected = {
            'preDelete': [DummyMixinWithAllHandlersClassPrepared._preDelete],
            'postDelete': [DummyMixinWithAllHandlersClassPrepared._postDelete, DummyMixinWithSingleHandlerPostDeleteClassPrepared._postDelete],
            'preSave': [DummyMixinWithAllHandlersClassPrepared._preSave],
            'postSave': [DummyMixinWithAllHandlersClassPrepared._postSave],
            'preInit': [DummyMixinWithAllHandlersClassPrepared._preInit],
            'postInit': [DummyMixinWithAllHandlersClassPrepared._postInit]
        }
        self.assertDictEqual(meta.handlerMap, expected, 'handlerMap should contain all of the expected handlers.')

