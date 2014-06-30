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
.. module:: informer
	:date: 06.30.2014
	:platform: Unix
	:synopsis: Python dependency graph Informer
	
.. moduleauthor:: Alex Braun <ABraunCCS@gmail.com>
'''
# ------------------------------------------------------------------------------

from collections import *

from axon.utilities.errors import *
from axon.utilities.utils import is_iterable
from axon.core.dg import Component
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
	
	def build(self, spec):
		self._spec = spec
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
		self.logs[name]['data'].append(message)
		self.master_log['data'].append(message)

		if self.state == 'active':
			if self.logs[name]['state'] == 'active':
				self.report(name)

	def report(self, log):
		last_line = self.logs[log]['data'][-1]
		if type(last_line) is str:
			print last_line
		else:
			# formatting is currently ad hoc
			# may be reimplemented as an automatic system
			fmt = '{:<18}  {:<35}'
			new_last_line = list(last_line)[2:]
			for line in new_last_line:
				fmt += '  {:<15}'
			print fmt.format(*last_line)
# ------------------------------------------------------------------------------

class NodeInformer(Informer):
	def __init__(self, spec, node):
		super(Informer, self).__init__(spec, node)
		self._cls = 'NodeInformer'
	# --------------------------------------------------------------------------
	
	@property
	def executor_log(self):
		return self.logs['executor']
	
	@property
	def ports_log(self):
		return self.logs['ports']

	@property
	def instruments_log(self):
		return self.logs['instruments']
# ------------------------------------------------------------------------------
	
class SceneInformer(Informer):
	def __init__(self, spec, node):
		super(Informer, self).__init__(spec, node)
		self._cls = 'SceneInformer'
	# --------------------------------------------------------------------------
	
	@property
	def sources_log(self):
		return self.logs['sources']

	@property
	def nodes_log(self):
		return self.logs['nodes']
# ------------------------------------------------------------------------------

def main():
	'''
	Run help if called directly
	'''
	
	import __main__
	help(__main__)
# ------------------------------------------------------------------------------

__all__ = ['Informer', 'NodeInformer', 'SceneInformer']

if __name__ == '__main__':
	main()