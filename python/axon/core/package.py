#! /usr/bin/env python
# Alex Braun 06.30.2014

# ------------------------------------------------------------------------------
# The MIT License (MIT)

# Copyright (c) 2014 Alex Braun

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# ------------------------------------------------------------------------------

'''
.. module:: package
    :date: 06.30.2014
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