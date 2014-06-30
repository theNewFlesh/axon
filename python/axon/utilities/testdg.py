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
.. module:: dg
	:date: 06.30.2014
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