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

from axon.utilities.errors import *
from axon.core.components.dg import DG
# ------------------------------------------------------------------------------

class Executor(Component):
	def __init__(self, spec, node):
		super(Executor, self).__init__(spec, node)
		self._cls = 'DG'
	# --------------------------------------------------------------------------
	
	def build(self, spec):
		self._spec = spec
		self._map['name'] = spec['name']
	# --------------------------------------------------------------------------
		
	def propagate_packages(self):
		# INFORMER HOOK
		message = 'propagate_packages', self.node.name
		self.node.informer.log('executor', message)
		# ----------------------------------------------------------------------

		outports = self.node.out_ports
		for outport in outports:
			connected_ports = outport.connected_ports
			for port in connected_ports:
				node = port.node
				executor = node.executor
				executor.update_packages()
				executor.update_node()

	def update_packages(self):
		# INFORMER HOOK
		message = 'update_packages', self.node.name
		self.node.informer.log('executor', message)
		# ----------------------------------------------------------------------

		node = self.node
		for port in node.in_ports:
			package = port.retrieve_package()
			package_name = port.get_package_name()
			node.set_package(package_name, package)
			port.change_state()

	def initialize_packages(self):
		# INFORMER HOOK
		message = 'initialize_packages', self.node.name
		self.node.informer.log('executor', message)
		# ----------------------------------------------------------------------

		for port in self.node.in_ports:
			if port.get_connected_port() == None:
				self.node.initialize_package(port.get_package_name())

	def generate_packages(self):
		# INFORMER HOOK
		message = 'generate_packages', self.node.name
		self.node.informer.log('executor', message)
		# ----------------------------------------------------------------------

		source = self.node.source_package.get_instance()
		target = self.node.target_package
		generate = self.node.generator_package.get_generator()	
		instance = generate(source)
		target.set_instance(instance)
	# --------------------------------------------------------------------------

	def get_state_of_in_ports(self):
		for port in self.node.in_ports:
			if port.get_state() == 'waiting':
				return 'waiting'
		return 'ready'

	def revert_in_port_states(self):
		for port in self.node.in_ports:
			port.change_state()

	def update_node(self):
		# INFORMER HOOK
		message = 'update_node', self.node.name
		self.node.informer.log('executor', message)
		# ----------------------------------------------------------------------

		if self.get_state_of_in_ports() == 'ready':
			self.revert_in_port_states()

			if self.node.source_package and self.node.target_package and self.node.generator_package:
				self.generate_packages()
			
			for ispec in self.node.instruments(registered_only=True):
				# INFORMER HOOK
				message = 'fire', self.node.name, self.name, self._args.values(), self._kwargs.values()
				self.node.informer.log('instruments', message)
				# ----------------------------------------------------------------------

				method = self.node.get_method method = ispec['method']
				args = [x['value'] for x in ispec['args']]
				kwargs = {}
				for kwarg in ispec['kwargs']:
					kwargs[kwarg] = kwarg['value']

				method(*args, **kwargs)

		method = self.node.get_package(self._package_name).get_method(self._method_name)
		method(*self._args.values(), **self._kwargs)

			for instrument in self.get_registered_instruments():
				instrument.fire()

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