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