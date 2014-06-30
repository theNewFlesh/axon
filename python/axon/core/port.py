#! /usr/bin/env python

# Alex Braun 01.25.2014
# >> INSERT LICENSE HERE <<

'''
.. module:: port
	:date: 01.25.2014
	:platform: Unix
	:synopsis: Node port
	
.. moduleauthor:: Alex Braun <ABraunCCS@gmail.com>
'''
# ------------------------------------------------------------------------------

import copy
from axon.utilities.errors import *
from axon.core.dg import Component
# ------------------------------------------------------------------------------

class InPort(Component):
	def __init__(self, spec, node):
		super(InPort, self).__init__(spec, node)
		self._cls = 'InPort'
	# --------------------------------------------------------------------------
	
	@property
	def type(self):
		return self._map['type']

	@property
	def package_name(self):
		return self._map['package_name']

	@property
	def connected_port(self):
		return self._map['connected_port']

	@property
	def state(self):
		self._map['state']
	# --------------------------------------------------------------------------

	def build(self, spec):
		self._spec = spec
		self._map['name'] = spec['name']
		self._map['type'] = spec['type']
		self._map['package_name'] = spec['package_name']
		self._map['connected_port'] = None
		self._map['state'] = spec['state']
	# --------------------------------------------------------------------------

	def set_state(self, state):
		self._map['state'] = state

	def change_state(self):
		if self.connected_port == None:
			self.set_state('ready')
		elif len(self.node.in_ports) < 2:
			self.set_state('ready')
		elif self.state == 'waiting':
			self.set_state('ready')
		else:
			self.set_state('waiting')
	# --------------------------------------------------------------------------

	def connect_port(self, port):
		# INFORMER HOOK
		message = 'connect_port', self.node.name, port.name
		self.node.informer.log('ports', message)
		# ----------------------------------------------------------------------

		# add in port to connected out port's connections dict
		port._add_connected_port(self)
		self.connected_port[port.name] = port
		executor = self.node.executor
		executor.update_packages()
		executor.update_node()
		executor.propagate_packages()

	def disconnect_port(self):
		# INFORMER HOOK
		message = 'disconnect_port', self.node.name
		self.node.informer.log('ports', message)
		# ----------------------------------------------------------------------

		# remove in port from previously connected out port's connections dict
		port = self.connected_port
		port._remove_connected_port(self)
		self.connected_port = None
		executor = self.node.executor
		executor.initialize_packages()
		executor.update_node()
		executor.propagate_packages()
	
	def retrieve_package(self):
		# INFORMER HOOK
		message = 'retrieve_package', self.node.name, self.package_name
		self.node.informer.log('ports', message)
		# ----------------------------------------------------------------------
		
		connected_port = self.connected_port
		if connected_port:
			node = connected_port.values().node
			package = node.all_packages[self.package.name]
			instance = node.all_packages[self.package.name].instance
			new_package = copy.copy(package)
			instance = copy.copy(package.instance)
			new_package.set_instance(instance)
			return new_package
			# return package
# ------------------------------------------------------------------------------

class OutPort(Component):
	def __init__(self, spec, node):
		super(OutPort, self).__init__(spec, node)
		self._cls = 'OutPort'
	# --------------------------------------------------------------------------

	@property
	def type(self):
		return self._map['type']

	@property
	def package_name(self):
		return self._map['package_name']

	@property
	def connected_ports(self):
		return self._map['connected_ports']
	# --------------------------------------------------------------------------

	def build(self, spec):
		self._spec = spec
		self._map['name'] = spec['name']
		self._map['type'] = spec['type']
		self._map['package_name'] = spec['package_name']
		self._map['connected_ports'] = {}
	# --------------------------------------------------------------------------

	def connect_port(self, port):
		self.connected_ports[port.name] = port

	def disconnect_port(self, port):
		del self.connected_ports[port.name]

	def send_package(self):
		for key, port in self.connected_ports.iteritems():
			port.retrieve_package()
# ------------------------------------------------------------------------------

def main():
	'''
	Run help if called directly
	'''
	
	import __main__
	help(__main__)
# ------------------------------------------------------------------------------

__all__ = ['InPort', 'OutPort']

if __name__ == '__main__':
	main()