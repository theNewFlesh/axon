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
scene_spec = {
'name': 'scene',
'informer': {
        'name': 'informer',
        'state': 'inactive',
        'logs': {
            'master': {
                'name': 'master',
                'state': 'inactive',
                'data': []},
            'nodes': {
                'name': 'nodes',
                'state': 'active',
                'data': [] }}},
'sources': {},
'nodes': {}
}

node_spec = {
    'name': 'example_node',
    'type': 'standard',
    'null': '<null>',
    'position': {
        'x': 1.0, 'y': 1.0, 'z':1.0, 't':1.0},
    'ports': {
        'in_ports': {
            'in': {
                'name': 'in',
                'type': 'in',
                'package_name': 'example_package',
                'connected_port': None,
                'state': 'ready'}},
        'out_ports': {
            'out': {
                'name': 'out',
                'type': 'out',
                'package_name': 'example_package',
                'connected_ports': {}}}
            },
    'executor': {
        'name':'executor'},
    'informer': {
        'name': 'informer',
        'state': 'active',
        'logs': {
            'master': {
                'name': 'master',
                'state': 'inactive',
                'data': []},
            'executor': {
                'name': 'executor',
                'state': 'active',
                'data': [] },
            'ports': {
                'name': 'ports',
                'state': 'inactive',
                'data': [] },
            'instruments': {
                'name': 'ports',
                'state': 'active',
                'data': [] }}},            
    'instruments': {
#         1: {
#             'set_data_instrument': {
#                 'name': 'set_data_instrument',
#                 'package_name': 'example_package',
#                 'method_name': 'set_data',
#                 'args': {
#                     1: {
#                         'data': {
#                             'name': 'data',
#                             'default': 123,
#                             'value': 123,
#                             'widget': '<spinbox>'}}},
#                 'kwargs': {} }}, 
        2: {
            'add_data_instrument': {
                'name': 'add_data_instrument',
                'package_name': 'example_package',
                'method_name': 'add_data',
                'args': {
                    1: {
                        'data': {
                            'name': 'data',
                            'default': 123,
                            'value': 123,
                            'widget': '<spinbox>' }}},
                'kwargs': {} }}}, 
        'packages': {
            'standard': {
                'example_package': {
                    'name': 'example_package',
                    'type': 'standard',
                    'source': {
                        'name': 'example',
                        'path': '~/google_drive/code/projects/axon/python/',
                        'module': 'axon.resources.example_model',
                        'class': 'Example'},
                    'class': '<Example>',
                    'instance': '<Example>',
                    'init_args': ['silly_example'],
                    'init_kwargs': {'data': 0},
                    'methods': {
                        'set_data': {
                            'args': {
                                1: {
                                    'data': {
                                        'name': 'data',
                                        'default': 123 }}},
                            'kwargs': {} },
                        'add_data': {
                            'args': {
                                1: {
                                    'data': {
                                        'name': 'data',
                                        'default': 321 }}},
                            'kwargs': {} }},
                    'data': {
                        'data': {
                            'name': 'data',
                            'attr': 'data',
                            'value': None},
                        'name': {
                            'name': 'name',
                            'attr': '_name',
                            'value': None }}}},
            'source': {},
            'generator': {},  
            'target': {} }
}