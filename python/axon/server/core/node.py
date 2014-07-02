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
.. module:: node
	:date: 06.30.2014
	:platform: Unix
	:synopsis: Python dependency graph node
	
.. moduleauthor:: Alex Braun <ABraunCCS@gmail.com>
'''
# ------------------------------------------------------------------------------

from collections import OrderedDict

from axon.utilities.errors import *
from axon.utilities.utils import *
from axon.server.core.dg import DG
from axon.server.core.executor import Executor
from axon.server.core.port import InPort, OutPort
from axon.server.core.instrument import Instrument
from axon.server.core.informer import NodeInformer
from axon.server.core.package import Package
# ------------------------------------------------------------------------------

class Node(DG):
	def __init__(self, spec, owner):
		super(Node, self).__init__(spec, owner)
		self._cls = 'Node'
	# --------------------------------------------------------------------------
	
	@property
	def type(self):
		return self._map['type']

	@property
	def null(self):
		return self._map['null']

	@property
	def executor(self):
		return self._map['executor']

	@property
	def informer(self):
		return self._map['informer']

	@property
	def ports(self):
		return self._map['ports']

	@property
	def all_ports(self):
		output = {}
		for type_ in self.ports:
			for key, port in self.ports[type_].iteritems():
				output[key] = port
		return output

	@property
	def in_ports(self):
		return self._map['ports']['in_ports']

	@property
	def out_ports(self):
		return self._map['ports']['out_ports']

	@property
	def packages(self):
		return self._map['packages']

	@property
	def all_packages(self):
		output = {}
		for type_ in self.packages:
			for name in self.packages[type_]:
				output[name] = self.packages[type_][name]
		return output

	@property
	def standard_packages(self):
		return self._map['packages']['standard']

	@property
	def source_package(self):
		return self._map['packages']['source']

	@property
	def generator_package(self):
		return self._map['packages']['generator']

	@property
	def target_package(self):
		return self._map['packages']['target']

	@property
	def instruments(self):
		return self._map['instruments']
	# --------------------------------------------------------------------------
	
	def build(self, spec):
		self._spec = spec
		self._map['executor'] = self.create_executor(spec['executor'])
		self._map['informer'] = self.create_informer(spec['informer'])
		self._map['name'] = spec['name']
		self._map['type'] = spec['type']
		self._map['null'] = spec['null']
		self._map['packages'] = {}
		self._map['ports'] = {}
		self._map['ports']['in_ports'] = {}
		self._map['ports']['out_ports'] = {}

		for type_, val in spec['packages'].iteritems():
			for k, pspec in val.iteritems():
				package = self.create_package(pspec)
				self._map['packages'][type_] = {}
				self._map['packages'][type_][package.name] = package

		self._map['instruments'] = OrderedDict()
		ispecs = spec_to_ordereddict(spec['instruments'])
		for key, ispec in ispecs.iteritems():
			instrument = self.create_instrument(ispec)
			self._map['instruments'][instrument.name] = instrument

		for inspec in spec['ports']['in_ports'].values():
			in_port = self.create_port(inspec)
			self._map['ports']['in_ports'][in_port.name] = in_port

		for outspec in spec['ports']['out_ports'].values():
			out_port = self.create_port(outspec)
			self._map['ports']['out_ports'][out_port.name] = out_port
	# --------------------------------------------------------------------------
	
	def create_executor(self, spec):
		executor = Executor(spec, self)
		return executor

	def create_informer(self, spec):
		informer = NodeInformer(spec, self)
		return informer

	def create_package(self, spec):
		package = Package(spec, self)
		return package

	def create_instrument(self, spec):
		instrument = Instrument(spec, self)
		return instrument

	def create_port(self, spec):
		if spec['type'] == 'in':
			return InPort(spec, self)
		elif spec['type'] == 'out':
			return OutPort(spec, self)
		else:
			raise TypeError('Invalid port type')
	# --------------------------------------------------------------------------

	def set_package(self, package_name, package):
		self.all_packages[package_name] = package
	# --------------------------------------------------------------------------

	def filter_by_name(self, spec, name):
		output = {}
		for key, val in spec.iteritems():
			if val.name == name:
				output[key] = val
		return output 

	def filter_by_type(self, spec, itype):
		output = {}
		for key, val in spec.iteritems():
			if val.type == itype:
				output[key] = val
		return output
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