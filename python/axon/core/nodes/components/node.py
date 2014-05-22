#! /usr/bin/env python

# Alex Braun 01.25.2014
# >> INSERT LICENSE HERE <<

'''
.. module:: node
	:date: 01.25.2014
	:platform: Unix
	:synopsis: Python dependency graph node
	
.. moduleauthor:: Alex Braun <ABraunCCS@gmail.com>
'''
# ------------------------------------------------------------------------------

from collections import OrderedDict

from axon.utilities.errors import *
from axon.dependency.graph.nodes.components.dg import DG
from axon.dependency.graph.nodes.components.executor import Executor
from axon.dependency.graph.nodes.components.port import *
from axon.dependency.graph.nodes.components.instrument import *
from axon.utilities.informer import Informer
# ------------------------------------------------------------------------------

class Node(DG):
	def __init__(self, name, owner=None, **options):
		super(Node, self).__init__(name, owner=owner, **options)
		self._class = 'Node'
		self._name = name
		self._owner = owner
		self._owner_node = self
		self._in_ports = {}
		self._out_ports = {}
		self._packages = {}
		self._package_library = {}
		self._source_package = None
		self._target_package = None
		self._generator_package = None
		self._instruments = {}
		self._executor = Executor(name + 'Executor', owner=self)
		self._informer = Informer(name + 'Informer', owner=self)
		self._informer.create_log('executor')
		self._informer.create_log('ports')
		self._informer.create_log('instruments')
		self._informer.activate_log('executor')
		self._informer.activate_log('ports')
		self._informer.activate_log('instruments')
	# --------------------------------------------------------------------------
	
	def add_in_port(self, name, package_name='~!package_name'):
		_check_kwargs(package_name)
		in_port = InPort(name, owner=self, package_name=package_name)
		self._in_ports[name] = in_port

	def get_in_port(self, name):
		return self._in_ports[name]

	def get_in_ports(self):
		return self._in_ports.values()

	def list_in_ports(self):
		for key, val in self._in_ports.iteritems():
			print key, ':', val

	def add_out_port(self, name, package_name='~!package_name'):
		_check_kwargs(package_name)
		out_port = OutPort(name, self, package_name)
		self._out_ports[name] = out_port

	def get_out_port(self, name):
		return self._out_ports[name]

	def get_out_ports(self):
		return self._out_ports.values()

	def list_out_ports(self):
		for key, val in self._out_ports.iteritems():
			print key, ':', val
	# --------------------------------------------------------------------------
	
	def get_package_from_library(self, name):
		return self._package_library[name]

	def get_packages_from_library(self):
		return self._package_library.values()

	def list_packages_from_library(self):
		for key, val in self._package_library.iteritems():
			print key, ':', val
	# --------------------------------------------------------------------------
	
	def initialize_package(self, name):
		package_class = self.get_package_from_library(name)
		self._packages[name] = package_class(name, owner=self)
	
	def register_package(self, name, package_class='~!package_class'):
		_check_kwargs(package_class)
		self._package_library[name] = package_class
		self.initialize_package(name)

	def get_package(self, name):
		return self._packages[name]

	def get_packages(self):
		return self._packages.values()                                                                         

	def list_packages(self):
		for key, val in self._packages.iteritems():
			print key, ':', val

	def set_package(self, name, package='~!package'):
		_check_kwargs(package)
		self._packages[name] = package
	# --------------------------------------------------------------------------
	
	def mark_source_package(self, name):
		self._source_package = name

	def get_source_package(self):
		if self._source_package:
			return self._packages[self._source_package]
		else:
			NotFound('Source Package not set')

	def mark_target_package(self, name):
		self._target_package = name

	def get_target_package(self):
		if self._target_package:
			return self._packages[self._target_package]
		else:
			NotFound('Target Package not set')

	def mark_generator_package(self, name):
		self._generator_package = name

	def get_generator_package(self):
		if self._generator_package:
			return self._packages[self._generator_package]
		else:
			NotFound('Generator Package not set')
	# --------------------------------------------------------------------------
	
	def get_executor(self):
		return self._executor

	def get_informer(self):
		return self._informer
	# --------------------------------------------------------------------------
	
	def add_instrument(self, name, package_name='~!package_name', method_name='~!method_name'):
		_check_kwargs(package_name, method_name)
		self._instruments[name] = Instrument(name, owner=self, package_name=package_name, method_name=method_name)

	def auto_add_instruments(self, package_name='~!package_name'):
		_check_kwargs(package_name)
		package = self.get_package(package_name)
		for spec in package.get_method_specs():
			self.add_instrument(spec['name'], package_name, spec['name'])
			instrument = self.get_instrument(spec['name'])
			instrument.auto_add_interfaces()

	def get_instrument(self, name):
		return self._instruments[name]

	def get_instruments(self):
		return self._instruments.values()

	def list_instruments(self):
		for key, val in self._instruments.iteritems():
			print key, ':', val
# ------------------------------------------------------------------------------

def main():
	'''
	Run help if called directly
	'''
	
	import __main__
	help(__main__)
# ------------------------------------------------------------------------------

__all__ = ['Node']

if __name__ == '__main__':
	main()