#! /usr/bin/env python

# Alex Braun 12.29.2013
# >> INSERT LICENSE HERE <<

'''
.. module:: errors
	:date: 12.29.2013
	:platform: Unix
	:synopsis: Library of error messages
	
.. moduleauthor:: Alex Braun <ABraunCCS@gmail.com>
'''
# ------------------------------------------------------------------------------

import re
# ------------------------------------------------------------------------------

class NotFound(Exception):
	def __init__(self, value):
		self._value = value
	def __str__(self):
		return repr(self._value)

class BadArgument(Exception):
	def __init__(self, value):
		self._value = value
	def __str__(self):
		return repr(self._value)

class OperatorError(Exception):
	def __init__(self, value):
		self._value = value
	def __str__(self):
		return repr(self._value)

class MissingKeywordArgument(Exception):
    def __init__(self, message):
        self._message = message
    def __str__(self):
        return self._message
    
def _check_kwargs(self, *kwargs):
    default_re = re.compile('~!')
    for kwarg in kwargs:
        if default_re.match(str(kwarg)):
            raise MissingKeywordArgument(kwarg[2:])
# ------------------------------------------------------------------------------

def main():
	'''
	Run help if called directly
	'''
	
	import __main__
	help(__main__)
# ------------------------------------------------------------------------------

__all__ = ['NotFound', 'BadArgument', 'OperatorError', 'MissingKeywordArgument', '_check_kwargs']

if __name__ == '__main__':
	main()