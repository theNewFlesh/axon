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
from axon.dependency.graph.nodes.components.dg import DG
# ------------------------------------------------------------------------------

class Package(DG):
    def __init__(self, name, owner=None, **options):
        super(Package, self).__init__(name, owner=owner, **options)
        self._class = 'Package'
        self._name = name
        self._owner = owner
        self._owner_node = owner
        self._instance = None
        self._method_specs = OrderedDict()
        self._data = {}
    # --------------------------------------------------------------------------
    
    def get_instance(self):
        return self._instance

    def set_instance(self, instance):
        self._instance = instance
    # --------------------------------------------------------------------------
    
    def add_datum(self, name):
        def func(temp):
            return eval('temp._instance.' + name)
        self._data[name] = func

    def add_data(self, names):
        for name in names:
            self.add_datum(name)

    def get_datum(self, name):
        return self._data[name](self)
        
    def get_data(self):
        values = []
        for datum in self._data.values():
            values.append(datum(self))
        return values

    def list_data(self):
        values = {}
        for key in self._data.keys():
            func = self._data[key]
            values[key] = func(self)
        return values
    # --------------------------------------------------------------------------
    
    def add_method_spec(self, method_spec):
        method = method_spec[0]
        _args = method_spec[1]
        _arg_defaults = method_spec[3]
        _arg_widgets = method_spec[5]
        _kwargs = method_spec[2]
        _kwarg_defaults = method_spec[4]
        _kwarg_widgets = method_spec[6]

        args = namedtuple('args', _args)
        args = args(*_arg_defaults)
        arg_widgets = namedtuple('arg_widgets', _args)
        arg_widgets = arg_widgets(*_arg_widgets)
        kwargs = namedtuple('kwargs', _kwargs)
        kwargs = kwargs(*_kwarg_defaults) 
        kwarg_widgets = namedtuple('kwarg_widgets', _kwargs)
        kwarg_widgets = kwarg_widgets(*_kwarg_widgets)
        
        spec = OrderedDict()
        spec['name'] = method
        spec['args'] = args
        spec['arg_widgets'] = arg_widgets
        spec['kwargs'] = kwargs
        spec['kwarg_widgets'] = kwarg_widgets
        self._method_specs[method] = spec

    def add_method_specs(self, method_spec_index):
        for method_spec in method_spec_index:
            self.add_method_spec(method_spec)

    def get_method_spec(self, name):
        return self._method_specs[name]

    def get_method_specs(self):
        return self._method_specs.values()

    def list_method_spec(self, name):
        for key, val in self._method_specs[name].iteritems():
            print key, ':', val

    def list_method_specs(self):
        for key, val in self._method_specs.iteritems():
            print key
            print self.list_method_spec(key)
    # --------------------------------------------------------------------------
    
    def add_method(self, name):
        spec = [name, [], [], [], [], [], [] ]
        self.add_method_spec(spec)

    def get_method(self, name):
        return getattr(self.get_instance(), name)

    def get_methods(self):
        for spec in self.get_method_specs():
            return getattr(self.get_instance(), spec['name'])
    # --------------------------------------------------------------------------
    
    def mark_generator_method(self, name):
        self._generator = self.get_method(name)

    def get_generator(self):
        return self._generator
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