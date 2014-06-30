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
from axon.utilities.utils import *
from axon.core.dg import DG
from axon.core.executor import Executor
from axon.core.port import InPort, OutPort
from axon.core.instrument import Instrument
from axon.core.informer import NodeInformer
from axon.core.package import Package
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