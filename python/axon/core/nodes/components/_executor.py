#! /usr/bin/env python

# Alex Braun 01.25.2014
# >> INSERT LICENSE HERE <<

'''
.. module:: executor
	:date: 01.25.2014
	:platform: Unix
	:synopsis: Python dependency graph event executor
	
.. moduleauthor:: Alex Braun <ABraunCCS@gmail.com>
'''
# ------------------------------------------------------------------------------

from collections import OrderedDict

from axon.utilities.errors import *
from axon.dependencygraph.nodes.components.dg import DG
# ------------------------------------------------------------------------------

class Executor(DG):
	def __init__(self, spec):
		super(Executor, self).__init__(spec)
		self._name = spec['name']
		self._registered_instruments = OrderedDict()
		self._callbacks = OrderedDict()
	# --------------------------------------------------------------------------
	
	def add_callback(self, name, callback):
		self._callbacks[name] = callback

	def remove_callback(self, name):
		del self._callbacks[name]

	def get_callback(self, name):
		return self._callbacks[name]

	def get_callbacks(self):
		return self._callbacks.values()
	# --------------------------------------------------------------------------
	
	def register_instrument(self, name):
		self._registered_instruments[name] = self.get_owner_node().get_instrument(name)

	def deregister_instrument(self, name):
		del self._registered_instruments[name]

	def get_registered_instruments(self):
		return self._registered_instruments.values() 

	def list_registered_instruments(self):
		for key, val in self._registered_instruments.iteritems():
			print key, ':', val
	# --------------------------------------------------------------------------

	def propagate_packages(self):
		# INFORMER HOOK
		message = 'propagate_packages', self.get_owner_node().get_name()
		self.get_owner_node().get_informer().log('executor', message=message)
		# ----------------------------------------------------------------------

		outports = self.get_owner_node().get_out_ports()
		for outport in outports:
			connected_ports = outport.get_connected_ports()
			for port in connected_ports:
				node = port.get_owner_node()
				executor = node.get_executor()
				executor.update_packages()
				executor.update_node()

	def update_packages(self):
		# INFORMER HOOK
		message = 'update_packages', self.get_owner_node().get_name()
		self.get_owner_node().get_informer().log('executor', message=message)
		# ----------------------------------------------------------------------

		node = self.get_owner_node()
		for port in node.get_in_ports():
			package = port.retrieve_package()
			package_name = port.get_package_name()
			node.set_package(package_name, package)
			port.change_state()

	def initialize_packages(self):
		# INFORMER HOOK
		message = 'initialize_packages', self.get_owner_node().get_name()
		self.get_owner_node().get_informer().log('executor', message=message)
		# ----------------------------------------------------------------------

		for port in self.get_owner_node().get_in_ports():
			if port.get_connected_port() == None:
				self.get_owner_node().initialize_package(port.get_package_name())

	def generate_packages(self):
		# INFORMER HOOK
		message = 'generate_packages', self.get_owner_node().get_name()
		self.get_owner_node().get_informer().log('executor', message=message)
		# ----------------------------------------------------------------------

		source = self.get_owner_node().get_source_package().get_instance()
		target = self.get_owner_node().get_target_package()
		generate = self.get_owner_node().get_generator_package().get_generator()	
		instance = generate(source)
		target.set_instance(instance)
	# --------------------------------------------------------------------------

	def get_state_of_in_ports(self):
		for port in self.get_owner_node().get_in_ports():
			if port.get_state() == 'waiting':
				return 'waiting'
		return 'ready'

	def revert_in_port_states(self):
		for port in self.get_owner_node().get_in_ports():
			port.change_state()

	def update_node(self):
		# INFORMER HOOK
		message = 'update_node', self.get_owner_node().get_name()
		self.get_owner_node().get_informer().log('executor', message=message)
		# ----------------------------------------------------------------------

		if self.get_state_of_in_ports() == 'ready':
			self.revert_in_port_states()

			if self.get_owner_node().get_source_package() and self.get_owner_node().get_target_package() and self.get_owner_node().get_generator_package():
				self.generate_packages()
			
			for ispec in self.get_owner_node().get_instruments(registered_only=True):
				# INFORMER HOOK
				message = 'fire', self.get_owner_node().get_name(), self.get_name(), self._args.values(), self._kwargs.values()
				self.get_owner_node().get_informer().log('instruments', message=message)
				# ----------------------------------------------------------------------

				method = self.get_owner_node().get_method method = ispec['method']
				args = [x['value'] for x in ispec['args']]
				kwargs = {}
				for kwarg in ispec['kwargs']:
					kwargs[kwarg] = kwarg['value']

				method(*args, **kwargs)

		method = self.get_owner_node().get_package(self._package_name).get_method(self._method_name)
		method(*self._args.values(), **self._kwargs)

			for instrument in self.get_registered_instruments():
				instrument.fire()

			for callback in self.get_callbacks():
				callback()

			self.propagate_packages()
# ------------------------------------------------------------------------------

def main():
	'''
	Run help if called directly
	'''
	
	import __main__
	help(__main__)
# ------------------------------------------------------------------------------

__all__ = ['Executor']

if __name__ == '__main__':
	main()