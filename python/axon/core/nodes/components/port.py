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
from collections import OrderedDict

from axon.utilities.errors import *
from axon.dependency.graph.nodes.components.dg import DG
# ------------------------------------------------------------------------------

class BasePort(DG):
	def __init__(self, name, owner=None, package_name='~!package_name', **options):
		super(BasePort, self).__init__(name, owner=owner, package_name=package_name, **options)
		_check_kwargs(package_name)
		self._class = 'BasePort'
		self._name = name
		self._owner = owner
		self._owner_node = owner
		self._package_name = package_name
		self._connected_port = None
	# --------------------------------------------------------------------------
	
	def get_package_name(self):
		return self._package_name

	def get_package(self):
		return self.get_owner_node().get_package(self.get_package_name())
# ------------------------------------------------------------------------------

class InPort(BasePort):
	def __init__(self, name, owner=None, package_name='~!package_name', **options):
		super(InPort, self).__init__(name, owner=owner, package_name=package_name, **options)
		_check_kwargs(package_name)
		self._class = 'InPort'
		self._name = name
		self._owner = owner
		self._owner_node = owner
		self._package_name = package_name
		self._connected_port = None
		self._state = 'ready'
	# --------------------------------------------------------------------------
	
	def connect_port(self, port):
		# INFORMER HOOK
		message = 'connect_port', self.get_owner_node().get_name(), port.get_name()
		self.get_owner_node().get_informer().log('ports', message=message)
		# ----------------------------------------------------------------------

		# add inPort to connected outPort's connections dict
		port._add_connected_port(self)
		self._connected_port = port
		executor = self.get_owner_node().get_executor()
		executor.update_packages()
		executor.update_node()
		executor.propagate_packages()

	def disconnect_port(self):
		# INFORMER HOOK
		message = 'disconnect_port', self.get_owner_node().get_name()
		self.get_owner_node().get_informer().log('ports', message=message)
		# ----------------------------------------------------------------------

		# remove inPort from previously connected outport's connections dict
		port = self._connected_port
		port._remove_connected_port(self)
		self._connected_port = None
		executor = self.get_owner_node().get_executor()
		executor.initialize_packages()
		executor.update_node()
		executor.propagate_packages()

	def get_connected_port(self):
		return self._connected_port
	
	def retrieve_package(self):
		# INFORMER HOOK
		message = 'retrieve_package', self.get_owner_node().get_name(), self.get_package_name()
		self.get_owner_node().get_informer().log('ports', message=message)
		# ----------------------------------------------------------------------
		
		package_name = self.get_package_name()
		connected_node = self.get_connected_port().get_owner_node()
		package = connected_node.get_package(package_name)
		instance = connected_node.get_package(package_name).get_instance()
		new_package = copy.copy(package)
		instance = copy.copy(package.get_instance())
		new_package.set_instance(instance)
		return new_package
		# return package
	# --------------------------------------------------------------------------

	def get_state(self):
		return self._state

	def change_state(self):
		if self._connected_port == None:
			self._state = 'ready'
		elif len( self.get_owner_node().get_in_ports() ) < 2:
			self._state = 'ready'
		elif self._state == 'waiting':
			self._state = 'ready'
		else:
			self._state = 'waiting'
# ------------------------------------------------------------------------------

class OutPort(BasePort):
	def __init__(self, name, owner=None, package_name='~!package_name', **options):
		super(OutPort, self).__init__(name, owner=owner, package_name=package_name, **options)
		_check_kwargs(package_name)
		self._class = 'OutPort'
		self._name = name
		self._owner = owner
		self._owner_node = owner
		self._package_name = package_name
		self._connected_ports = {}
	# --------------------------------------------------------------------------
	
	def _add_connected_port(self, port):
		self._connected_ports[port.get_name()] = port

	def _remove_connected_port(self, port):
		del self._connected_ports[port.get_name()]

	def get_connected_port(self, name):
		return self._connected_ports[name]

	def get_connected_ports(self):
		return self._connected_ports.values()

	def list_connected_ports(self):
		for key, val in self._connected_ports.iteritems():
			print key, ':', val

	def send_package(self):
		for port in self.get_connected_ports():
			port.retrieve_package()
# ------------------------------------------------------------------------------

def main():
	'''
	Run help if called directly
	'''
	
	import __main__
	help(__main__)
# ------------------------------------------------------------------------------

__all__ = ['BasePort', 'InPort', 'OutPort']

if __name__ == '__main__':
	main()