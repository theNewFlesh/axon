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
	def __init__(self, spec):
		super(Node, self).__init__(spec)
		self._class = 'Node'
		self._name = spec['name']
		self._spec = None
		self._map = None
		self.build()
		self._map['executor'] = self.create_executor(self.spec['executor'])
		self._map['informer'] = self.create_executor(self.spec['informer'])
		self.informer.create_log('executor')
		self.informer.create_log('ports')
		self.informer.create_log('instruments')
		self.informer.activate_log('executor')
		self.informer.activate_log('ports')
		self.informer.activate_log('instruments')
	# --------------------------------------------------------------------------
	
	def build(self):
		spec = self._spec
		self._type = spec['type']
		for pspec in spec['packages']:
			package = self.create_package(pspec)
			self._map['packages'][package['name']] = package

		for ispec in package['instruments']:
			instrument = self.create_instrument(ispec)
			self._map['instruments'][instrument['name']] = insrument

		for inspec in spec['ports']['in_ports']:
			in_port = self.create_port(inspec)
			self._map['ports']['in_ports']['name']] = in_port

		for outspec in spec['ports']['out_ports']:
			out_port = self.create_port(outspec)
			self._map['ports']['out_ports']['name']] = out_port

	def create_executor(self, spec):
		executor = Executor(spec)
		return executor

	def create_informer(self, spec):
		informer = Informer(spec)
		return informer

	def create_package(self, spec):
		spec['init'] = spec['class'](*spec['init_args'], **spec['init_kwargs'])
		package = Package(spec)
		return package

	def create_instrument(self, spec):
		instrument = Instrument(spec)
		return instrument

	def create_port(self, spec):
		if spec['type'] == 'in':
			port = InPort(spec)
			return port
		elif spec['type'] == 'out':
			port = OutPort(spec)
			return port
		else:
			raise TypeError('Invalid port type')
	# --------------------------------------------------------------------------
	
	@property
	def spec(self):
		return self._spec

	@propoerty
	def map(self):
		return self._map

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
	def in_ports(self):
		return self._map['ports']['in_ports']

	@property
	def out_ports(self):
		ports = self._map['ports']['out_ports']

	@property
	def packages(self):
		return self._map['packages']

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