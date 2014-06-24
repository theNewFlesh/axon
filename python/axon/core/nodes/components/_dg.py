#! /usr/bin/env python

# Alex Braun 01.25.2014
# >> INSERT LICENSE HERE <<

'''
.. module:: dg
	:date: 01.25.2014
	:platform: Unix
	:synopsis: Python dependency graph base
	
.. moduleauthor:: Alex Braun <ABraunCCS@gmail.com>
'''
# ------------------------------------------------------------------------------

from collections import OrderedDict

from axon.utilities.errors import *
from axon.utilities.utilities import Base
# ------------------------------------------------------------------------------

class DG(Base):
	def __init__(self, spec):
		super(DG, self).__init__()
		self._cls = 'DG'
		self._spec = spec
		self._map = {}
		self.build()
	# --------------------------------------------------------------------------
	
	@property
	def cls(self):
		return self._cls

	@property
	def spec(self):
		return self._spec

	@property
	def map(self):
		return self._map
	
	@property
	def name(self):
		return self._map['name']
	# --------------------------------------------------------------------------
	
	def build(self):
		self._map['name'] = self._spec['name']
# ------------------------------------------------------------------------------

class Component(Base):
	def __init__(self, spec, node):
		super(Component, self).__init__(spec)
		self._cls = 'Component'
		self._node = node
	# --------------------------------------------------------------------------
	
	@property
	def node(self):
		return self._node
# ------------------------------------------------------------------------------

def main():
	'''
	Run help if called directly
	'''
	
	import __main__
	help(__main__)
# ------------------------------------------------------------------------------

__all__ = ['DG', 'Component']

if __name__ == '__main__':
	main()