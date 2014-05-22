#! /usr/bin/env python

# Alex Braun 01.25.2014
# >> INSERT LICENSE HERE <<

'''
.. module:: instrument
	:date: 01.25.2014
	:platform: Unix
	:synopsis: Python dependency graph instrument
	
.. moduleauthor:: Alex Braun <ABraunCCS@gmail.com>
'''
# ------------------------------------------------------------------------------

from collections import *

from axon.utilities.errors import *
from axon.dependency.graph.nodes.components.dg import DG
# ------------------------------------------------------------------------------

class Instrument(DG):
	def __init__(self, name, owner=None, package_name='~!package_name', 
				method_name='~!method_name', **options):
		super(Instrument, self).__init__(name, owner=owner, **options)
		_check_kwargs(package_name, method_name)
		self._class = 'Instrument'
		self._name = name
		self._owner = owner
		self._owner_node = owner
		self._package_name = package_name
		self._method_name = method_name
		self._spec = self.get_owner_node().get_package(package_name).get_method_spec(method_name)		
		self._arg_defaults = self._spec['args']
		self._kwarg_defaults = self._spec['kwargs']
		self._args = self._spec['args']._asdict()
		self._kwargs = self._spec['kwargs']._asdict() 
		self._interfaces = OrderedDict()
	# --------------------------------------------------------------------------
	
	def fire(self):
		# INFORMER HOOK
		message = 'fire', self.get_owner_node().get_name(), self.get_name(), self._args.values(), self._kwargs.values()
		self.get_owner_node().get_informer().log('instruments', message=message)
		# ----------------------------------------------------------------------

		method = self.get_owner_node().get_package(self._package_name).get_method(self._method_name)
		method(*self._args.values(), **self._kwargs)
	# --------------------------------------------------------------------------
	
	def get_spec(self):
			return self._spec

	def list_spec(self):
		for item in spec.values():
			print i
	# --------------------------------------------------------------------------
	
	def get_args(self):
		return self._args

	def list_args(self):
		args = namedtuple('args', self._args)
		return args(*self._args.values())

	def get_kwargs(self):
		return self._kwargs

	def list_kwargs(self):
		kwargs = namedtuple('kwargs', self._kwargs)
		return kwargs(*self._kwargs.values())
	# --------------------------------------------------------------------------
	
	def add_interface(self, name, parameter='~!parameter', group_type='~!group_type', widget_type=None):
		_check_kwargs(parameter, group_type)
		self._interfaces[name] = Interface(name, owner=self, parameter=parameter, group_type=group_type)

	def auto_add_interfaces(self):
		for arg_name in self.get_args():
			widget_type = self.get_spec()['arg_widgets']._asdict()[arg_name]
			self.add_interface(arg_name, parameter=arg_name, group_type='args', widget_type=widget_type)
		
		for kwarg_name in self.get_kwargs():
			widget_type = self.get_spec()['kwarg_widgets']._asdict()[kwarg_name]
			self.add_interface(kwarg_name, parameter=kwarg_name, group_type='kwargs', widget_type=widget_type)

	def get_interface(self, name):
		return self._interfaces[name]

	def get_interfaces(self):
		return self._interfaces.values()

	def list_interfaces(self):
		for key, val in self._interfaces.iteritems():
			print key, ':', val
	# --------------------------------------------------------------------------
	
	def register(self):
		self.get_owner_node().get_executor().register_instrument(self.get_name(), instrument=self)

	def deregister(self):
		self.get_owner_node().get_executor().deregister_instrument(self.get_name())
# ------------------------------------------------------------------------------

class Interface(DG):
	def __init__(self, name, owner=None, parameter='~!parameter', group_type='args', widget_type=None, **options):
		super(Interface, self).__init__(name, owner=owner, **options)
		_check_kwargs(parameter, group_type)
		self._class = 'Interface'
		self._name = name
		self._owner = owner
		self._owner_node = owner.get_owner_node()
		self._group_type = group_type
		self._parameter = parameter
		if self._group_type == 'kwargs':
			self._parameter_group= self.getOwner()._kwargs
		else:
			self._parameter_group= self.getOwner()._args	
		self._widget_type = widget_type
	# --------------------------------------------------------------------------
	
	def get_parameter(self):
		return self._parameter_group[self._parameter]

	def set_parameter(self, value=None):
		# INFORMER HOOK
		message = 'set_parameter', self.get_owner_node().get_name(), self.get_name(), value
		self.get_owner_node().get_informer().log('instruments', message=message)
		# ----------------------------------------------------------------------
	
		self._parameter_group[self._parameter] = value
		executor = self.get_owner_node().get_executor()
		executor.update_node()
# ------------------------------------------------------------------------------

def main():
	'''
	Run help if called directly
	'''
	
	import __main__
	help(__main__)
# ------------------------------------------------------------------------------

__all__ = ['Instrument', 'Interface']

if __name__ == '__main__':
	main()