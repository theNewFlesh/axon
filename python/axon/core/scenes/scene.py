#! /usr/bin/env python

# Alex Braun 01.25.2014
# >> INSERT LICENSE HERE <<

'''
.. module:: scene
	:date: 01.25.2014
	:platform: Unix
	:synopsis: Dependency graph scene
	
.. moduleauthor:: Alex Braun <ABraunCCS@gmail.com>
'''
# ------------------------------------------------------------------------------

import re
import copy

from axon.core.components.dg import DG
from axon.utilities.informer import Informer
# ------------------------------------------------------------------------------

class Scene(DG):
	def __init__(self, spec):
		super(Scene, self).__init__(spec)
		self._cls = 'Scene'
	# --------------------------------------------------------------------------

	@property
	def informer(self):
		return self._map['informer']

	@property
	def source_library(self):
		return self._map['source_library']

	@property
	def nodes(self):
		return self._map['nodes']
	# --------------------------------------------------------------------------

	def build(self, spec):
		self._map['name'] = spec['name']
		self._map['informer'] = self.create_informer(self.spec['informer'])
		self._map['source_library'] = spec['source_library']
		self._map['nodes'] = spec['nodes']
	# --------------------------------------------------------------------------

	def create_node_name(self, name):
		node_re = re.compile(name)
		num = 1
		for key in self.nodes:
			found = node_re.search(key)
			if found:
				num += 1
		return name + str(num)

	def create_node(self, spec):
		spec['name'] = self.create_node_name(spec['name'])

		# INFORMER HOOK
		message = 'create_node', spec['name']
		self.informer.log('node', message)
		# ----------------------------------------------------------------------

		for pspec in spec['packages']:
			pspec['init'] = self.get_class(pspec['class'])

		node = Node(spec)
		self.nodes[node.name] = node
		return node

	def destroy_node(self, node_name):
		del self.nodes[node_name]

	def update_instruments(self, spec, node):
		node = self.nodes[spec['name']]
		node.update_instruments(spec)

	def update_informer(self, spec, node):
		node = self.nodes[spec['name']]
		node.update_informer(spec)

	def rebuild(self, spec, node):
		node = self.nodes[spec['name']]
		node.build(spec)

	def connect_ports(self, out_port, in_port):	
		# INFORMER HOOK
		message = ('connect_ports', out_port.node.name,
		out_port.name, in_port.node.name, in_port.name)
		self.informer.log('node', message)
		# ----------------------------------------------------------------------
		
		in_port.connect_port(out_port)

	def disconnect_port(self, in_port):
		# INFORMER HOOK
		message = 'disconnect_port', in_port.node.name, in_port.name
		self.informer.log('node', message)
		# ----------------------------------------------------------------------

		in_port.disconnect_port()
# ------------------------------------------------------------------------------

def main():
	'''
	Run help if called directly
	'''
	
	import __main__
	help(__main__)
# ------------------------------------------------------------------------------

__all__ = ['Scene']

if __name__ == '__main__':
	main()