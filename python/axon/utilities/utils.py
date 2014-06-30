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
.. module:: utils
	:date: 06.30.2014
	:platform: Unix
	:synopsis: Library of utilities
	
.. moduleauthor:: Alex Braun <ABraunCCS@gmail.com>
'''
# ------------------------------------------------------------------------------

import re
from collections import OrderedDict
# ------------------------------------------------------------------------------

class Base(object):
	'''
	Dummy class for argument passing
	'''
	
	def __init__(self):
		self._cls = 'Base'

	@property
	def cls(self):
		return self._cls

	def _print_public(self):
		non_public_re = re.compile('^_')
		for item in dir(self):
			found = non_public_re.match(item)
			if not found:
				print item

	def _print_semi_private(self):
		semi_private_re = re.compile('^_[^_]+')
		for item in dir(self):
			found = semi_private_re.match(item)
			if found:
				print item

	def _print_private(self):
		private_re = re.compile('^__')
		for item in dir(self):
			found = private_re.match(item)
			if found:
				print item
# ------------------------------------------------------------------------------

def is_iterable(item):
	try:
		result = iter(item)
	except TypeError:
		return False
	return True

def spec_to_ordereddict(spec):
    order = sorted(spec.keys())
    new_dict = OrderedDict()
    for key in order:
        temp = spec[key]
        new_key = temp.keys()[0]
        new_val = temp[new_key]
        new_dict[new_key] = new_val
    return new_dict
# ------------------------------------------------------------------------------

def main():
	'''
	Run help if called directly
	'''
	
	import __main__
	help(__main__)
# ------------------------------------------------------------------------------

__all__ = ['Base', 'is_iterable', 'spec_to_ordereddict']

if __name__ == '__main__':
	main()