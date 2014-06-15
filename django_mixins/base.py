
import six

import django.db.models.base as djbase

from .utils import InstanceDescriptorMixin
from .auth import CurrentUser


class ModelBase(djbase.Model):

    class Meta:

        abstract = True


class MixinMeta(djbase.ModelBase):

    def __new__(cls, name, bases, attrs):

        # all mixins are abstract
        supernew = super(MixinMeta, cls).__new__

        class Meta:

            abstract = True

        attrs['Meta'] = Meta

        return supernew(cls, name, bases, attrs)


class MixinBase(djbase.Model, InstanceDescriptorMixin, six.with_metaclass(MixinMeta)):

    class Meta:

        abstract = True

