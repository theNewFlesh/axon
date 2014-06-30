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
.. module:: spec_editor
	:date: 06.30.2014
	:platform: Unix
	:synopsis: JSON specification editor
	
.. moduleauthor:: Alex Braun <ABraunCCS@gmail.com>
'''
# ------------------------------------------------------------------------------

from axon.utilities.errors import *
from axon.utilities.utils import *
from axon.core.dg import DG
# ------------------------------------------------------------------------------

class SpecEditor(DG):
	def __init__(self, spec, owner):
		super(SpecEditor, self).__init__(spec, owner)
		self._cls = 'Node'	
	# --------------------------------------------------------------------------

	def build(self, spec):
		self._spec = spec
		self._map = spec

	@property
	def name(self):
		return self._map['name']

	@property
	def type(self):
		return self._map['type']

	@property
	def null(self):
		return self._map['null']

	@property
	def position(self):
		return self._map['position']

	@property
	def ports(self):
		return self._map['ports']

	@property
	def executor(self):
		return self._map['executor']

	@property
	def informer(self):
		return self._map['informer']

	@property
	def instruments(self):
		return self._map['instruments']

	@property
	def packages(self):
		return self._map['packages']

	def add(self, component):
		pass

	def remove(self, component):
		pass

	def edit(self, component):
		pass
	
	def set(self, item, value):
		self._map[item] = value






































