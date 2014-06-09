#! /usr/bin/env python

# Alex Braun 01.25.2014
# >> INSERT LICENSE HERE <<

'''
.. module:: example_spec
    :date: 01.25.2014
    :platform: Unix
    :synopsis: Example Axon node specification
    
.. moduleauthor:: Alex Braun <ABraunCCS@gmail.com>
'''
# ------------------------------------------------------------------------------


spec = {
    'name': 'foobar_node',
    'type': 'standard',
    'position': {
        'x': 1.0, 'y': 1.0, 'z':1.0, 't':1.0},
    'ports': {
        'in_ports': {
            'in': {
                'name': 'in',
                'type': 'in',
                'package': 'foobar_package',
                'connected_ports': [] }},
        'out_ports': {
            'out': {
                'name': 'out',
                'type': 'out',
                'package': 'foobar_package',
                'connected_ports': [] }}
            },
    'executor': None,
    'informer': None,
    'instruments': {
        1: {
            'name': 'bar_instrument',
            'package': 'foobar',
            'method': 'bar'},
        2: {
            'name': 'foo_instrument',
            'package': 'foobar',
            'method': 'foo'}},
    'packages': {
            'standard': {
                'foobar_package': {
                    'name': 'foobar_package',
                    'type': 'standard',
                    'class': 'Foobar',
                    'init': None,
                    'init_args': [],
                    'init_kwargs': [],
                    'methods': {
                        'bar': {
                            'args': {
                                'arg1': {
                                    'default': [],
                                    'value': [5, 6],
                                    'widget': 'spinbox'},
                                'arg2': {
                                    'default': 1, 
                                    'value': 8, 
                                    'widget': 'numberfield'}},
                            'kwargs': {
                                'kwarg1': {
                                    'default': False,
                                    'value': True,
                                    'widget': 'radiobutton'}}},
                        'foo': {
                            'args': {
                                'arg1': {
                                    'default': [],
                                    'value': [10, 20],
                                    'widget': 'spinbox'},
                                'arg2': {
                                    'default': 1, 
                                    'value': 2, 
                                    'widget': 'numberfield'}},
                            'kwargs': {
                                'kwarg1': {
                                    'default': True,
                                    'value': False,
                                    'widget': 'radiobutton'}}}},
                'data': None}},
                'source': None,
                'generator': None,
                'target': None},
}
