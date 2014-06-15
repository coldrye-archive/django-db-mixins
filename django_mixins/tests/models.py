

from django.db.models import fields

from django_mixins import *

class SignalHandlerTestMixin(MixinBase):

    field = fields.TextField(default = None, null = True)

    @classmethod
    def _preDelete(cls, model, instance=None, using=None, **extraargs):

        pass

    @classmethod
    def _postDelete(cls, model, instance=None, using=None, **extraargs):

        pass

    @classmethod
    def _preSave(cls, model, instance=None, raw=False, using=None, update_fields=None, **extraargs):

        pass

    @classmethod
    def _postSave(cls, model, instance=None, created=False, raw=False, using=None, update_fields=None, **extraargs):

        pass


class SignalHandlerTestModel(ModelBase, SignalHandlerTestMixin):

    pass


class CreationMixinTestModel(ModelBase, CreationMixin):

    pass


class ModificationMixinTestModel(ModelBase, ModificationMixin):

    field = fields.TextField(default = None, null = True)


class SystemDefinableMixinTestModel(ModelBase, SystemDefinableMixin):

    field = fields.TextField(default = None, null = True)

