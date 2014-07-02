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
.. module:: port
	:date: 06.30.2014
	:platform: Unix
	:synopsis: Node port
	
.. moduleauthor:: Alex Braun <ABraunCCS@gmail.com>
'''
# ------------------------------------------------------------------------------

from axon.utilities.errors import *
from axon.server.core.dg import Component
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

	def connect(self, port):
		# INFORMER HOOK
		message = 'connect', self.node.name, port.name
		self.node.informer.log('ports', message)
		# ----------------------------------------------------------------------

		# add in port to connected out port's connections dict
		port.connect_port(self)
		self._map['connected_port'] = port
		executor = self.node.executor
		executor.update_packages()
		executor.update_node()

	def disconnect(self):
		# INFORMER HOOK
		message = 'disconnect', self.node.name
		self.node.informer.log('ports', message)
		# ----------------------------------------------------------------------

		# remove in port from previously connected out port's connections dict
		port = self.connected_port
		port.disconnect_port(self)
		self._map['connected_port'] = None
		executor = self.node.executor
		executor.rebuild_packages()
		executor.update_node()
		executor.propagate_packages()
	
	def retrieve_instance(self):
		# INFORMER HOOK
		message = 'retrieve_package', self.node.name, self.package_name
		self.node.informer.log('ports', message)
		# ----------------------------------------------------------------------
		
		if self.connected_port:
			node = self.connected_port.node
			instance = node.all_packages[self.package_name].instance
			return instance
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