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
            'bar_instrument': {
            'name': 'bar_instrument',
            'package': 'foobar',
            'method': 'bar',
            'args': {
                1: {
                    'arg1': {
                        'name': 'arg1',
                        'default': [],
                        'value': [5, 6],
                        'widget': 'spinbox'},
                2: {
                    'arg2': {
                        'name': 'arg2',
                        'default': 1, 
                        'value': 8, 
                        'widget': 'numberfield'}}}},
            'kwargs': {
                1: {
                    'kwarg1': {
                        'name': 'kwarg1',
                        'default': False,
                        'value': True,
                        'widget': 'radiobutton'}}}}},
        2: {
            'foo_instrument': {
            'name': 'foo_instrument',
            'package': 'foobar',
            'method': 'foo',
            'args': {
                1: {
                    'arg1': {
                        'name': 'arg1',
                        'default': [],
                        'value': [10, 20],
                        'widget': 'spinbox'}},
                2: {
                    'arg2': {
                        'name': 'arg2',
                        'default': 1, 
                        'value': 2, 
                        'widget': 'numberfield'}}},
            'kwargs': {
                1:{
                    'kwarg1': {
                        'name': 'kwarg1',
                        'default': True,
                        'value': False,
                        'widget': 'radiobutton'}}}}}},
    'packages': {
            'standard': {
                'foobar_package': {
                    'name': 'foobar_package',
                    'type': 'standard',
                    'class': 'Foobar',
                    'instance': '<<foobar>>',
                    'init_args': [1, 2, '<<foobar_arg_3>>'],
                    'init_kwargs': [],
                    'methods': {
                        'bar': {
                            'args': {
                                1: {
                                    'arg1': {
                                        'name': 'arg1',
                                        'default': []}},
                                2: {
                                    'arg2': {
                                        'name': 'arg2',
                                        'default': 1}}},
                            'kwargs': {
                                1: {
                                    'kwarg1': {
                                        'name': 'kwarg1',
                                        'default': False}}}},
                        'foo': {
                            'args': {
                                1: {
                                    'arg1': {
                                        'name': 'arg1',
                                        'default': []}},
                                2: {    
                                    'arg2': {
                                        'name': 'arg2',
                                        'default': 1}}},
                            'kwargs': {
                                1: {
                                    'kwarg1': {
                                        'name': 'kwarg1',
                                        'default': True}}}}},
                'data': {
                    'some_data': 'data'}}},
                'source': None,
                'generator': None,
                'target': None}
}
