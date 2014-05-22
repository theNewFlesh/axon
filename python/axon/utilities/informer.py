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
from axon.dependency.graph.nodes.components.dg import DG
# ------------------------------------------------------------------------------

class Informer(DG):
	def __init__(self, name, owner=None, **options):
		super(Informer, self).__init__(name, owner=owner, **options)
		self._state = 'inactive'
		self._master_log = []
		self._logs = OrderedDict()
		self._active_logs = set()
	# --------------------------------------------------------------------------
	
	def activate(self):
		self._state = 'active'

	def deactivate(self):
		self._state = 'inactive'

	def switch_state(self):
		if self._state == 'active':
			self._state = 'inactive'
		else:
			self._state = 'active'
	# --------------------------------------------------------------------------

	def create_log(self, name):
		self._logs[name] = []

	def get_log(self, name):
		return self._logs[name]

	def get_master_log(self):
		return self._master_log	

	def print_log(self, name):
		for line in self.get_log(name):
			print line

	def print_master_log(self, name):
		for line in self.get_master_log():
			print line
	# --------------------------------------------------------------------------

	def log(self, name, message='~!message'):
		_check_kwargs(message)
		self._logs[name].append(message)
		self._master_log.append(message)

		if self._state == 'active':
			if name in self._active_logs:
				self.report(name)

	def report(self, log_name='~!log_name'):
		last_line = self.get_log(log_name)[-1]
		if type(last_line) is str:
			print self.get_log(log_name)[-1]
		elif is_iterable(last_line):
			# formatting is currently ad hoc
			# may be reimplemented as an automatic system
			fmt = '{:<17}  {:<35}'
			new_last_line = list(last_line)[2:]
			for line in new_last_line:
				fmt += '  {:<15}'
			print fmt.format(*last_line)
		else:
			print last_line 

	def activate_log(self, name):
		self._active_logs.add(name)

	def deactivate_log(self, name):
		self._active_logs.remove(name)

	def activate_all_logs(self):
		for log in self._logs:
			self.activate_log(log)

	def deactivate_all_logs(self):
		self._active_logs.clear()

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