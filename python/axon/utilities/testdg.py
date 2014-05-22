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
	def __init__(self, navigation_map, name=None, owner=None, **options):
		super(DG, self).__init__(**options)
		self._class = 'DG'
		self._name = name
		self._owner = owner
		self._nav = navigation_map
	# --------------------------------------------------------------------------
	
	def get_class(self):
		return self._class

	def get_name(self):
		return self._name
	
	@property
	def nav(self):
		return self._nav

	def nav_up(self):
		return self._nav['owner']

	def nav_down(self):
		return self._nav['children']

	def nav_to(self, destination):
		return self._nav[destination]

	def nav_up_until(self, condition):
		def _nav_up_until(node):
			owner = node.owner
			try:
				if condition(owner):
					return owner
				else:
					_nav_up_until(owner)
			except:
				raise NotFound('Owner not found')
		return _nav_up_until(self)

	def nav_down_until(self, condition):
		def _nav_down_until(node):
			children = node.nav_down()
			for child in children:
				if condition(child):
					return child
				else:
					try:
						_nav_down_until(child)
					except:
						pass
			raise NotFound('Child not found')
		return _nav_down_until(self)

# ------------------------------------------------------------------------------

def main():
	'''
	Run help if called directly
	'''
	
	import __main__
	help(__main__)
# ------------------------------------------------------------------------------

__all__ = ['DG']

if __name__ == '__main__':
	main()