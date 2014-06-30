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
from axon.core.dg import Component
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

    @property
    def data(self):
        for name, spec in self._map['data'].iteritems():
            datum = self.create_attribute(spec)()
            self._map['data'][name]['value'] = datum
        return self._map['data']
    # --------------------------------------------------------------------------

    def build(self, spec):
        self._spec = spec
        self._map['name'] = spec['name']
        self._map['type'] = spec['type']
        self._map['class'] = spec['class']
        self._map['init_args'] = spec['init_args']
        self._map['init_kwargs'] = spec['init_kwargs']
        self._map['data'] = spec['data']
        self._map['instance'] = self.create_instance()
        self._map['methods'] = {}
        self.build_methods(spec)

    def build_methods(self, spec):
        for mspec in spec['methods']:
            method = self.create_method(mspec)
            self._map['methods'][mspec] = method
    # --------------------------------------------------------------------------
        
    def create_instance(self):
        instance = self.class_(*self.init_args, **self.init_kwargs)
        return instance

    def create_method(self, spec):
        method = getattr(self.instance, spec)
        return method

    def create_attribute(self, spec):
        attr = spec['attr']
        def func():
            return getattr(self.instance, attr)
        return func
    # --------------------------------------------------------------------------
        
    def set_instance(self, instance):
        self._map['instance'] = instance
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