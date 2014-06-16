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
from collections import OrderedDict

from axon.utilities.errors import _check_kwargs
from axon.dependency.graph.nodes.components.dg import DG
from axon.utilities.informer import Informer
# ------------------------------------------------------------------------------

class Scene(DG):
	def __init__(self, name, source_library, owner=None):
		super(Scene, self).__init__(name, owner=owner)
		self._class = 'Scene'
		self._name = name
		self._owner = owner
		self._source_library = source_library
		self._nodes = OrderedDict()
		
	def create_node_name(self, name):
		node_re = re.compile(name)
		num = 1
		for key in self._nodes:
			found = node_re.search(key)
			if found:
				num += 1
		return name + str(num)

	def create_node(self, spec):
		spec['name'] = self.create_node_name(spec['name'])

		# INFORMER HOOK
		message = 'create_node', spec['name']
		self.get_informer().log('node', message=message)
		# ----------------------------------------------------------------------

		for pspec in spec['packages']:
			pspec['init'] = self.get_class(pspec['class'])

		node = Node(spec)
		self._nodes[node.name] = node
		return node

	def destroy_node(self, node_name):
		del self._nodes[node_name]

	def get_node(self, node_name):
		return self._nodes[node_name]

	def list_nodes(self):
		for key, val in self._nodes.iteritems():
			print key, ':', val	

	def connect_ports(self, out_port, in_port):	
		# INFORMER HOOK
		message = ('connect_ports', out_port.get_owner_node().get_name(),
		out_port.get_name(), in_port.get_owner_node().get_name(), in_port.get_name() )
		self.get_informer().log('node', message=message)
		# ----------------------------------------------------------------------
		
		in_port.connect_port(out_port)

	def disconnect_ports(self, in_port):
		# INFORMER HOOK
		message = 'disconnect_ports', in_port.get_owner_node().get_name(), in_port.get_name()
		self.get_informer().log('node', message=message)
		# ----------------------------------------------------------------------

		in_port.disconnect_port()

	def reform_spec(self, spec):
		spec['class'] = self._source_library[spec['class']]
		return spec

	def get_node_spec(self, node_name):
		node = self._nodes[node_name]
		spec = copy(node.get_spec())
		spec = self.reform_spec(spec)
		return spec

	def set_node_spec(self, node_name, spec):
		node = self.get_node(node_name)
		node.set_spec(spec)

	def update_node(self, node_name, spec):
		node = self.get_node(node_name)
		node.update_spec(spec)
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