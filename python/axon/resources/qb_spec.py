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
.. module:: qb_spec
    :date: 06.30.2014
    :platform: Unix
    :synopsis: qb node specification
    
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
    'name': 'qb_node',
    'type': 'standard',
    'null': '<null>',
    'position': {
        'x': 1.0, 'y': 1.0, 'z':1.0, 't':1.0},
    'ports': {
        'in_ports': {
            'in': {
                'name': 'in',
                'type': 'in',
                'package': 'qb_package',
                'connected_port': None,
                'state': 'ready'}},
        'out_ports': {
            'out': {
                'name': 'out',
                'type': 'out',
                'package': 'qb_package',
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
                'state': 'inactive',
                'data': [] }}},            
    'instruments': {
         1: {
             'jobinfo_instrument': {
                 'name': 'jobinfo_instrument',
                 'package_name': 'qb_package',
                 'method_name': 'jobinfo',
                 'args': {},
                 'kwargs': {
                     1: {
                         'filters': {
                             'name': 'filters',
                             'default': {},
                             'value': {},
                             'widget': '<textbox>'}},
                     2: {
                         'agenda': {
                             'name': 'agenda',
                             'default': True,
                             'value': {},
                             'widget': '<radiobutton>'}},
                     3: {
                         'subjobs': {
                             'name': 'subjobs',
                             'default': False,
                             'value': {},
                             'widget': '<radiobutton>'}}}}}},
        'packages': {
            'standard': {
                 'qb_package': {
                     'name': 'qb_package',
                     'type': 'standard',
                     'source': {
                         'name': 'qb',
                         'path': '~/google_drive/code/projects/sparse/python/',
                         'module': 'sparse.utilities.mock',
                         'class': 'qb'},
                     'class': '<qb>',
                     'instance': '<qb>',
                     'init_args': [],
                     'init_kwargs': {'name': None},
                     'methods': {
                         'jobinfo': {
                             'args': {},
                             'kwargs': {
                                 1: {
                                     'filters': {
                                         'name': 'filters',
                                         'default': {} }},
                                 2: {
                                     'agenda': {
                                         'name': 'agenda',
                                         'default': True}},
                                 3: {
                                     'subjobs': {
                                         'name': 'subjobs',
                                         'default': False}}}}},
                     'data': {
                         'jobs': None }}},
            'source': None,
            'generator': None,  
            'target': None}
}