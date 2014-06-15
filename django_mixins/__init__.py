
import inspect
import sys

from django.dispatch import receiver
from django.db.models.signals import (class_prepared, pre_init, post_init, 
                                      pre_delete, post_delete, pre_save, 
                                      post_save)

from .base import MixinBase, ModelBase

__all__ = [
    'CreationMixin', 'ModificationMixin', 'ModelRefMixin', 
    'SystemDefinableMixin', 'MixinBase', 'ModelBase'
]


def _registerSignalReceivers(model):

    def callSignalHandler(signalName, model, **kwargs):

        handlerName = '_' + signalName
        handlers = model._mixinMeta.handlerMap.get(signalName, None)
        if handlers:

            for handler in handlers:

                handler(model, **kwargs)

    signals = {
        'preInit' : pre_init, 'postInit' : post_init,
        'preDelete' : pre_delete, 'postDelete' : post_delete,
        'preSave' : pre_save, 'postSave' : post_save
    }
    for name, signal in signals.items():

        if model._mixinMeta.handlerMap.get(name, None):

            def factory(name, signal):

                def signalHandler(sender, **kwargs):

                    callSignalHandler(name, sender, **kwargs)

                return receiver(signal, sender=model)(signalHandler)

            model._mixinMeta.receivers[name] = factory(name, signal)


_signals = (
    'preInit', 'postInit',
    'preDelete', 'postDelete',
    'preSave', 'postSave'
)
_handlerNames = set(['_' + signal for signal in _signals])

@receiver(class_prepared)
def classPreparedReceiver(sender, **kwargs):

    model = sender
    if issubclass(model, MixinBase):

        mixinMeta = type(model.__name__ + 'Meta', (object,), {
            'receivers' : {},
            'handlerMap' : dict(((signal, None) for signal in _signals))
        })

        handlerName = '_classPrepared' 
        basesSeen = []
        for base in inspect.getmro(model):

            if (base in (model, MixinBase)
                or hasattr(base, '_meta') and 
                (base._meta.abstract and not issubclass(base, MixinBase))):

                continue

            if issubclass(base, MixinBase):

                # we must not add the handlers of derived mixin's bases
                # as these are reponsible for calling the 'overwritten'
                # handlers of their base classes
                baseWasSubclassed = False
                for seen in basesSeen:

                    if issubclass(seen, base):

                        baseWasSubclassed = True
                        break

                if baseWasSubclassed:

                        continue

                basesSeen.append(base)

                if hasattr(base, handlerName):

                    handler = getattr(base, handlerName)
                    handler(model, **kwargs)

                for name in _handlerNames.intersection(set(base.__dict__.keys())):

                    signal = name[1:]
                    handlers = mixinMeta.handlerMap.get(signal, None)
                    if handlers is None:

                        handlers = []
                        mixinMeta.handlerMap[signal] = handlers

                    handlers.append(getattr(base, name))

        setattr(model, '_mixinMeta', mixinMeta)

        _registerSignalReceivers(model)


from .mixins import CreationMixin, ModificationMixin
from .modelref import ModelRefMixin
from .systemdefinable import SystemDefinableMixin

