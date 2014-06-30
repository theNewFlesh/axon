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
from axon.core.dg import Component
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

		for outport in self.node.out_ports.values():
			for port in outport.connected_ports.values():
				node = port.node
				executor = node.executor
				executor.update_packages()
				executor.update_node()

	def update_packages(self):
		# INFORMER HOOK
		message = 'update_packages', self.node.name
		self.node.informer.log('executor', message)
		# ----------------------------------------------------------------------

		for port in self.node.in_ports.values():
			package = port.retrieve_package()
			self.node.set_package(port.package_name, package)
			port.change_state()

	def reinitialize_packages(self):
		# INFORMER HOOK
		message = 'reinitialize_packages', self.node.name
		self.node.informer.log('executor', message)
		# ----------------------------------------------------------------------

		for port in self.node.in_ports.values():
			if port.connected_port == None:
				package = self.node.all_packages[port.package_name]
				package.reinitialize()

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

	@property
	def state_of_in_ports(self):
		for port in self.node.in_ports.values():
			if port.state == 'waiting':
				return 'waiting'
		return 'ready'

	def revert_in_port_states(self):
		for port in self.node.in_ports.values():
			port.change_state()

	def update_node(self):
		# INFORMER HOOK
		message = 'update_node', self.node.name
		self.node.informer.log('executor', message)
		# ----------------------------------------------------------------------

		if self.state_of_in_ports == 'ready':
			self.revert_in_port_states()

			if self.node.type == 'generator':
				self.generate_packages()

			for instrument in self.node.instruments.values():
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