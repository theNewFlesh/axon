#! /usr/bin/env python

# Alex Braun 01.25.2014
# >> INSERT LICENSE HERE <<

'''
.. module:: package
    :date: 01.25.2014
    :platform: Unix
    :synopsis: Node package
    
.. moduleauthor:: Alex Braun <ABraunCCS@gmail.com>
'''
# ------------------------------------------------------------------------------

from collections import *

from axon.utilities.errors import *
from axon.core.components.dg import Component
# ------------------------------------------------------------------------------

class Package(Component):
    def __init__(self, spec, node):
        super(Package, self).__init__(spec, node)
        self._cls = 'Package'
    # --------------------------------------------------------------------------

    @property
    def class_(self):
        return self._map['class']

    @property
    def instance(self):
        return self._map['instance']

    @property
    def init_args(self):
        return self._map['init_args']

    @property
    def init_kwargs(self):
        return self._map['init_kwargs']

    @property
    def methods(self):
        return self._map['methods']
    # --------------------------------------------------------------------------

    def build(self, spec):
        self._spec = spec
        self._map['name'] = spec['name']
        self._map['type'] = spec['type']
        self._map['class'] = spec['class']
        self._map['init_args'] = spec['init_args']
        self._map['init_kwargs'] = spec['init_kwargs']
        self._map['instance'] = self.create_instance()

        for mspec in self._spec['methods']:
            method = self.create_method(mspec)
            self._map['methods'][method.name] = method

        for dspec in self._spec['data']:
            datum = self.create_datum(dspec)
            self._map['data'][dspec] = datum
    # --------------------------------------------------------------------------
        
    def set_instance(self, instance):
        self._map['instance'] = instance

    def create_instance(self):
        return self.class_(*self.init_args, **self.init_kwargs)

    def create_method(self, spec):
        return getattr(self.instance, spec)

    def create_datum(self, spec):
        def func():
            return getattr(self.instance, spec)
        return func
# ------------------------------------------------------------------------------

def main():
    '''
    Run help if called directly
    '''
    
    import __main__
    help(__main__)
# ------------------------------------------------------------------------------

__all__ = ['Package']

if __name__ == '__main__':
    main()