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
	def __init__(self, spec, owner):
		super(DG, self).__init__()
		self._cls = 'DG'
		self._spec = {}
		self._map = {}
		self._owner = owner
		self.build(spec)
	# --------------------------------------------------------------------------
	
	@property
	def spec(self):
		return self._spec

	@property
	def map(self):
		return self._map
	
	@property
	def name(self):
		return self._map['name']

	@property
	def owner(self):
		return self._owner
	# --------------------------------------------------------------------------
	
	def build(self, spec):
		self._spec = spec
		self._map['name'] = self._spec['name']
# ------------------------------------------------------------------------------

class Component(DG):
	def __init__(self, spec, owner):
		super(Component, self).__init__(spec, owner)
		self._cls = 'Component'
	# --------------------------------------------------------------------------
	
	@property
	def node(self):
		return self._owner
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