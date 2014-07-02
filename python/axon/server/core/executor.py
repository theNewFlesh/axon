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
.. module:: executor
	:date: 06.30.2014
	:platform: Unix
	:synopsis: Python dependency graph event executor
	
.. moduleauthor:: Alex Braun <ABraunCCS@gmail.com>
'''
# ------------------------------------------------------------------------------

import copy
from axon.utilities.errors import *
from axon.server.core.dg import Component
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
				executor = port.node.executor
				executor.update_packages()
				executor.update_node()

	def update_packages(self):
		# INFORMER HOOK
		message = 'update_packages', self.node.name
		self.node.informer.log('executor', message)
		# ----------------------------------------------------------------------

		for port in self.node.in_ports.values():
			instance = port.retrieve_instance()
			# Not using copy sort of works but ruins the date of all preceding nodes
			instance = copy.copy(instance)
			package = self.node.all_packages[port.package_name]
			package.set_instance(instance)
			package.build_methods(package.spec)
			port.change_state()

	def rebuild_packages(self):
		# INFORMER HOOK
		message = 'rebuild_packages', self.node.name
		self.node.informer.log('executor', message)
		# ----------------------------------------------------------------------

		for port in self.node.in_ports.values():
			if port.connected_port == None:
				package = self.node.all_packages[port.package_name]
				package.build(package.spec)

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