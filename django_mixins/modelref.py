

from django.db.models import fields

from .base import MixinBase


class ModelRefMixin(MixinBase):

    refmodel = fields.TextField()
    refmodelid = fields.IntegerField()

    _cachedModelRef = None

    @property
    def modelRef(self):

        if not self._cachedModelRef and self.refmodel and self.refmodelid:

            #
            # get model class for self.refmodel
            # get model instance for self.refmodelid
            # self._cachedModelRef = ...
            #
            pass

        return self._cachedModelRef

    @modelRef.setter
    def _setModelRef(self, model):

        if model and model != self._cachedModelRef:

            self.refmodel = model.__class__
            self.refmodelid = model.id
            self._cachedModelRef = model

