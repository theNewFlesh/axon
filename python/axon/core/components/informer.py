#! /usr/bin/env python

# Alex Braun 01.25.2014
# >> INSERT LICENSE HERE <<

'''
.. module:: informer
	:date: 01.25.2014
	:platform: Unix
	:synopsis: Python dependency graph Informer
	
.. moduleauthor:: Alex Braun <ABraunCCS@gmail.com>
'''
# ------------------------------------------------------------------------------

from collections import *

from axon.utilities.errors import *
from axon.utilities.utilities import is_iterable
from axon.core.components.dg import Component
# ------------------------------------------------------------------------------

class Informer(Component):
	def __init__(self, spec, node):
		super(Informer, self).__init__(spec, node)
		self._cls = 'Informer'
	# --------------------------------------------------------------------------
	
	@property
	def state(self):
		return self._map['state']

	@property
	def logs(self):
		return self._map['logs']

	@property
	def master_log(self):
		return self.logs['master']

	@property
	def executor_log(self):
		return self.logs['executor']
	
	@property
	def ports_log(self):
		return self.logs['ports']

	@property
	def instruments_log(self):
		return self.logs['instruments']
	
	@property
	def active_logs(self):
		output = {}
		for log in self.logs:
			if log['state'] == 'active':
				output[log] = self.logs[log]
		return output

	@property
	def inactive_logs(self):
		output = {}
		for log in self.logs:
			if log['state'] == 'inactive':
				output[log] = self.logs[log]
		return output
	# --------------------------------------------------------------------------
	
	def build(self):
		spec = self._spec
		self._map['name'] = spec['name']
		self._map['state'] = spec['state']
		self._map['logs'] = spec['logs']
	# --------------------------------------------------------------------------

	def activate(self):
		self._map['state'] = 'active'

	def deactivate(self):
		self._map['state'] = 'inactive'

	def switch_state(self):
		if self._map['state'] == 'active':
			self._map['state'] = 'inactive'
		else:
			self._map['state'] = 'active'
	# --------------------------------------------------------------------------

	def log(self, name, message):
		self.logs[name]['date'].append(message)
		self.master_log['date'].append(message)

		if self.state == 'active':
			if self.logs['name']['state'] == 'active':
				self.report(name)

	def report(self, log_name):
		last_line = self.logs(log_name)['data'][-1]
		if type(last_line) is str:
			print last line
		else: is_iterable(last_line):
			# formatting is currently ad hoc
			# may be reimplemented as an automatic system
			fmt = '{:<17}  {:<35}'
			new_last_line = list(last_line)[2:]
			for line in new_last_line:
				fmt += '  {:<15}'
			print fmt.format(*last_line)
# ------------------------------------------------------------------------------

def main():
	'''
	Run help if called directly
	'''
	
	import __main__
	help(__main__)
# ------------------------------------------------------------------------------

__all__ = ['Informer']

if __name__ == '__main__':
	main()