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
	def __init__(self, name, owner=None, **options):
		super(DG, self).__init__(**options)
		self._class = 'DG'
		self._name = name
		self._owner = owner
	# --------------------------------------------------------------------------
	
	def get_class(self):
		return self._class

	def get_name(self):
		return self._name

	def get_owner(self):
		return self._owner

	def get_owner_node(self):
		return self._ownerNode
		
	def get_owner_by_class(self, class_name):
		def _get_owner_by_class(node):
			owner = node.get_owner()
			if node.get_class() != class_name:
				_get_owner_node(owner)
			elif node.get_class() == class_name:
				return owner
			else:
				raise NotFound('Owner node not found')
		return _get_owner_by_class(self)
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